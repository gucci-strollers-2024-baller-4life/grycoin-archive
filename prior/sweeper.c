/* sweeper.c - exhaustive case-flip sweeper for the demo block.
 *
 * Design notes that differ from the usual recipe, because the box is what it is:
 *   - `nproc` is 1 in this sandbox, so OpenMP buys nothing. Single threaded, but written so that
 *     `-fopenmp` can be dropped in on a wider machine by removing the #ifdef guard.
 *   - there is no libcrypto on this image, so MD5 is implemented inline (RFC 1321). No dependency.
 *   - no malloc in the search loop: every context is a stack struct copied by value.
 *   - the real speed comes from the cascade, not from the compiler: because every candidate shares
 *     the same 1,549-byte base and differs in at most K bytes, the MD5 state is precomputed at every
 *     candidate position, and each inner iteration only re-hashes from the previous edit forward.
 *
 * usage: sweeper [base] [pool] [anchor] [prefix] [k]
 *   base    raw text, hashed byte for byte
 *   pool    eligible positions, one decimal index per line
 *   anchor  fixed edits, one "<index> <char>" per line (applied before enumeration)
 *   prefix  hex prefix the md5 must start with, e.g. 3c6
 *   k       number of free edits to enumerate (2 or 3)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

/* ---------- MD5 ---------- */
typedef struct { uint32_t h[4]; uint8_t buf[64]; uint64_t len; size_t n; } md5_t;

static const uint32_t K[64] = {
0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391};
static const uint8_t SH[64] = {
7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21};

static inline uint32_t rotl(uint32_t x, uint8_t c){ return (x<<c)|(x>>(32-c)); }

static void md5_block(uint32_t h[4], const uint8_t p[64]){
  uint32_t m[16], a=h[0], b=h[1], c=h[2], d=h[3], f, t; int i, g;
  for(i=0;i<16;i++) m[i] = (uint32_t)p[i*4] | ((uint32_t)p[i*4+1]<<8) | ((uint32_t)p[i*4+2]<<16) | ((uint32_t)p[i*4+3]<<24);
  for(i=0;i<64;i++){
    if(i<16){ f=(b&c)|(~b&d); g=i; }
    else if(i<32){ f=(d&b)|(~d&c); g=(5*i+1)&15; }
    else if(i<48){ f=b^c^d; g=(3*i+5)&15; }
    else { f=c^(b|~d); g=(7*i)&15; }
    t=d; d=c; c=b;
    b = b + rotl(a + f + K[i] + m[g], SH[i]);
    a = t;
  }
  h[0]+=a; h[1]+=b; h[2]+=c; h[3]+=d;
}

static void md5_init(md5_t *x){ x->h[0]=0x67452301;x->h[1]=0xefcdab89;x->h[2]=0x98badcfe;x->h[3]=0x10325476;x->len=0;x->n=0; }

static void md5_update(md5_t *x, const uint8_t *p, size_t l){
  x->len += (uint64_t)l;
  if(x->n){
    size_t need = 64 - x->n, take = l < need ? l : need;
    memcpy(x->buf + x->n, p, take); x->n += take; p += take; l -= take;
    if(x->n == 64){ md5_block(x->h, x->buf); x->n = 0; }
  }
  while(l >= 64){ md5_block(x->h, p); p += 64; l -= 64; }
  if(l){ memcpy(x->buf, p, l); x->n = l; }
}

static void md5_final(md5_t x, uint8_t out[16]){
  uint64_t bits = x.len * 8; uint8_t pad[72]; size_t padlen;
  padlen = (x.n < 56) ? (56 - x.n) : (120 - x.n);
  memset(pad, 0, padlen); pad[0] = 0x80;
  { uint8_t tmp[8]; int i; for(i=0;i<8;i++) tmp[i] = (uint8_t)(bits >> (8*i)); memcpy(pad+padlen, tmp, 8); }
  { md5_t y = x; md5_update(&y, pad, padlen+8);
    { int i; for(i=0;i<4;i++){ out[i*4]=(uint8_t)y.h[i]; out[i*4+1]=(uint8_t)(y.h[i]>>8); out[i*4+2]=(uint8_t)(y.h[i]>>16); out[i*4+3]=(uint8_t)(y.h[i]>>24);} } }
}

/* ---------- helpers ---------- */
static int hexcmp(const uint8_t d[16], const char *pre){
  static const char *H="0123456789abcdef"; size_t L=strlen(pre); size_t i;
  for(i=0;i<L;i++){
    char a = H[(d[i/2] >> (i%2?0:4)) & 0xF];
    if(a != pre[i]) return 1;
  }
  return 0;
}
static int clampi(int v,int lo,int hi){ return v<lo?lo:(v>hi?hi:v); }

int main(int argc,char**argv){
  if(argc<6){ fprintf(stderr,"usage: %s base pool anchor prefix k\n",argv[0]); return 2; }
  FILE *f=fopen(argv[1],"rb");
  if(!f){ perror("base"); return 2; }
  fseek(f,0,SEEK_END); long len=ftell(f); fseek(f,0,SEEK_SET);
  uint8_t *base=malloc(len+96); if(fread(base,1,len,f)!=(size_t)len){ return 2; } fclose(f);
  memset(base+len,0,96);

  /* anchors */
  f=fopen(argv[3],"r");
  if(f){ int idx; char ch;
    while(fscanf(f,"%d %c",&idx,&ch)==2){ if(idx>=0&&idx<len) base[idx]=(uint8_t)ch; }
    fclose(f);
  }

  /* pool */
  int cap=4096, npool=0, *pool=malloc(sizeof(int)*cap);
  f=fopen(argv[2],"r");
  if(!f){ perror("pool"); return 2; }
  { int v; while(fscanf(f,"%d",&v)==1){ if(npool==cap){ cap*=2; pool=realloc(pool,sizeof(int)*cap);} pool[npool++]=v; } }
  fclose(f);

  const char *prefix=argv[4];
  int k=atoi(argv[5]);
  if(k<1||k>4){ fprintf(stderr,"k must be 1..4\n"); return 2; }

  /* precompute the md5 state before each pool byte */
  md5_t *st = malloc(sizeof(md5_t)*npool);
  { md5_t run; md5_init(&run); int pos=0, i;
    for(i=0;i<npool;i++){
      int p=pool[i];
      if(p<pos){ fprintf(stderr,"pool not sorted at %d\n",i); return 2; }
      if(p>pos){ md5_update(&run, base+pos, (size_t)(p-pos)); pos=p; }
      st[i]=run;                       /* state before consuming byte p */
    }
  }

  long long cands=0, hits=0; int i1,i2,i3,i4;
  clock_t t0=clock();
  uint8_t dig[16];
  char hexbuf[33];
  FILE *out=fopen("sweeper_hits.txt","w");

  #define FLIP(b) ((b>=97&&b<=122)?(uint8_t)(b-32):((b>=65&&b<=90)?(uint8_t)(b+32):(b)))

  if(k==3){
    for(i1=0;i1<npool;i1++){
      md5_t c1=st[i1]; uint8_t f1=FLIP(base[pool[i1]]); md5_update(&c1,&f1,1);
      int p1=pool[i1];
      for(i2=i1+1;i2<npool;i2++){
        int p2=pool[i2];
        md5_t c2=c1; md5_update(&c2, base+p1+1, (size_t)(p2-p1-1));
        uint8_t f2=FLIP(base[p2]); md5_update(&c2,&f2,1);
        for(i3=i2+1;i3<npool;i3++){
          int p3=pool[i3];
          md5_t c3=c2; md5_update(&c3, base+p2+1, (size_t)(p3-p2-1));
          uint8_t f3=FLIP(base[p3]); md5_update(&c3,&f3,1);
          md5_update(&c3, base+p3+1, (size_t)(len-p3-1));
          md5_final(c3,dig); cands++;
          if(hexcmp(dig,prefix)==0){
            hits++;
            { int j; for(j=0;j<16;j++) sprintf(hexbuf+j*2,"%02x",dig[j]); }
            fprintf(out,"%s %d %d %d\n",hexbuf,pool[i1],pool[i2],pool[i3]);
            fflush(out);
          }
        }
      }
    }
  } else if(k==2){
    for(i1=0;i1<npool;i1++){
      md5_t c1=st[i1]; uint8_t f1=FLIP(base[pool[i1]]); md5_update(&c1,&f1,1);
      int p1=pool[i1];
      for(i2=i1+1;i2<npool;i2++){
        int p2=pool[i2];
        md5_t c2=c1; md5_update(&c2, base+p1+1, (size_t)(p2-p1-1));
        uint8_t f2=FLIP(base[p2]); md5_update(&c2,&f2,1);
        md5_update(&c2, base+p2+1, (size_t)(len-p2-1));
        md5_final(c2,dig); cands++;
        if(hexcmp(dig,prefix)==0){
          hits++;
          { int j; for(j=0;j<16;j++) sprintf(hexbuf+j*2,"%02x",dig[j]); }
          fprintf(out,"%s %d %d\n",hexbuf,pool[i1],pool[i2]); fflush(out);
        }
      }
    }
  } else { fprintf(stderr,"only k=2,3 implemented\n"); return 2; }

  double dt=(double)(clock()-t0)/CLOCKS_PER_SEC;
  printf("candidates %lld  prefix hits %lld  time %.2fs  rate %.2f M/s\n",
         cands, hits, dt, cands/dt/1e6);
  fclose(out);
  return 0;
}
