/* Unrestricted k=4 case-flip sweep over every alpha position of a base text,
   ordinal-range sharded. Midstate incremental MD5. Prints md5-prefix-3c6 hits.
   usage: k4global <basefile> <startOrdinal> <endOrdinal> <outfile> [maxSeconds] */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct { uint32_t s[4]; uint64_t n; uint8_t buf[64]; uint32_t bl; } ctx;
static const uint32_t K[64]={0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391};
static const uint32_t S[64]={7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21};
static inline uint32_t rl(uint32_t x,uint32_t n){return (x<<n)|(x>>(32-n));}
static void mi(ctx*c){c->s[0]=0x67452301u;c->s[1]=0xefcdab89u;c->s[2]=0x98badcfeu;c->s[3]=0x10325476u;c->n=0;c->bl=0;}
static void mb(ctx*c,const uint8_t*p){uint32_t m[16];for(int i=0;i<16;i++)m[i]=(uint32_t)p[4*i]|((uint32_t)p[4*i+1]<<8)|((uint32_t)p[4*i+2]<<16)|((uint32_t)p[4*i+3]<<24);
uint32_t a=c->s[0],b=c->s[1],cc=c->s[2],d=c->s[3],f,t;int g;
for(int i=0;i<64;i++){if(i<16){f=(b&cc)|(~b&d);g=i;}else if(i<32){f=(d&b)|(~d&cc);g=(5*i+1)&15;}
else if(i<48){f=b^cc^d;g=(3*i+5)&15;}else{f=cc^(b|~d);g=(7*i)&15;}t=a+f+K[i]+m[g];a=d;d=cc;cc=b;b=b+rl(t,S[i]);}
c->s[0]+=a;c->s[1]+=b;c->s[2]+=cc;c->s[3]+=d;}
static void mu(ctx*c,const uint8_t*p,size_t n){c->n+=n;if(c->bl){size_t need=64-c->bl;if(n<need){memcpy(c->buf+c->bl,p,n);c->bl+=n;return;}
memcpy(c->buf+c->bl,p,need);mb(c,c->buf);p+=need;n-=need;c->bl=0;}
while(n>=64){mb(c,p);p+=64;n-=64;}if(n){memcpy(c->buf,p,n);c->bl=n;}}
static void mf(const ctx*c,uint8_t o[16]){ctx t=*c;uint64_t bits=t.n<<3;uint8_t pad[72];uint32_t rem=t.bl,pl=(rem<56)?(56-rem):(120-rem);
memset(pad,0,sizeof pad);pad[0]=0x80;for(int i=0;i<8;i++)pad[pl+i]=(uint8_t)(bits>>(8*i));mu(&t,pad,pl+8);
for(int i=0;i<4;i++){o[4*i]=(uint8_t)t.s[i];o[4*i+1]=(uint8_t)(t.s[i]>>8);o[4*i+2]=(uint8_t)(t.s[i]>>16);o[4*i+3]=(uint8_t)(t.s[i]>>24);}}
static uint64_t C2(uint64_t n,int k){ if(k==1)return n; if(k==2)return n*(n-1)/2; if(k==3)return n*(n-1)*(n-2)/6; if(k==4)return n*(n-1)*(n-2)*(n-3)/24; return 0;}
int main(int argc,char**argv){
 if(argc<5){fprintf(stderr,"usage: %s base start end out [maxsec]\n",argv[0]);return 2;}
 FILE*f=fopen(argv[1],"rb");fseek(f,0,SEEK_END);long L=ftell(f);fseek(f,0,SEEK_SET);
 uint8_t*base=malloc(L);if(fread(base,1,L,f)!=(size_t)L)return 2;fclose(f);
 uint64_t s0=strtoull(argv[2],0,10), e0=strtoull(argv[3],0,10);
 int maxsec=argc>5?atoi(argv[5]):0;
 FILE*out=fopen(argv[4],"a");
 int pos[8192],n=0;
 for(long i=0;i<L;i++){uint8_t c=base[i];if((c>='A'&&c<='Z')||(c>='a'&&c<='z'))pos[n++]=(int)i;}
 uint64_t total=C2(n,4); if(e0>total)e0=total;
 /* unrank s0 -> i,j,k,l */
 uint64_t rem=s0; int i0=0;
 while(i0<n-4 && C2(n-i0-1,3)<=rem){rem-=C2(n-i0-1,3);i0++;}
 int j0=i0+1;
 while(j0<n-3 && C2(n-j0-1,2)<=rem){rem-=C2(n-j0-1,2);j0++;}
 int k0=j0+1;
 while(k0<n-2 && (uint64_t)(n-k0-1)<=rem){rem-=(uint64_t)(n-k0-1);k0++;}
 int l0=k0+1+(int)rem;
 fprintf(stderr,"n=%d total=%llu range=%llu..%llu start=(%d,%d,%d,%d)\n",n,(unsigned long long)total,
   (unsigned long long)s0,(unsigned long long)e0,i0,j0,k0,l0);
 ctx*st=malloc(sizeof(ctx)*n);{ctx run;mi(&run);long cur=0;
  for(int q=0;q<n;q++){mu(&run,base+cur,pos[q]-cur);ctx t=run;uint8_t c=base[pos[q]]^0x20;mu(&t,&c,1);st[q]=t;cur=pos[q];}}
 uint64_t want=e0-s0, done=0, hits=0;
 struct timespec t0,t1;clock_gettime(CLOCK_MONOTONIC,&t0);
 int i=i0,j,k,l,first_i=1;
 for(;i<n-3;i++){
  ctx ci=st[i];
  j = first_i ? j0 : i+1; first_i=0;
  int first_j=1;
  for(;j<n-2;j++){
   ctx cij=ci; mu(&cij,base+pos[i]+1,pos[j]-pos[i]-1);
   uint8_t fj=base[pos[j]]^0x20; mu(&cij,&fj,1);
   k = first_j ? k0 : j+1; first_j=0;
   int first_k=1;
   for(;k<n-1;k++){
    ctx cijk=cij; mu(&cijk,base+pos[j]+1,pos[k]-pos[j]-1);
    uint8_t fk=base[pos[k]]^0x20; mu(&cijk,&fk,1);
    l = first_k ? l0 : k+1; first_k=0;
    int cur=pos[k]+1;
    for(;l<n;l++){
     ctx c4=cijk; mu(&c4,base+cur,pos[l]-cur);
     uint8_t fl=base[pos[l]]^0x20; mu(&c4,&fl,1); mu(&c4,base+pos[l]+1,(size_t)(L-pos[l]-1));
     uint8_t d[16]; mf(&c4,d); done++;
     if(d[0]==0x3c&&(d[1]>>4)==0x6){hits++;fprintf(out,"%d %d %d %d ",pos[i],pos[j],pos[k],pos[l]);
      for(int q=0;q<16;q++)fprintf(out,"%02x",d[q]);fprintf(out,"\n");}
     cur=pos[l]+1;
     if(done>=want)goto finished;
    }
   }
  }
  clock_gettime(CLOCK_MONOTONIC,&t1);
  double el=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)/1e9;
  if(maxsec&&el>maxsec){fprintf(stderr,"TIMECUT done=%llu hits=%llu at i=%d\n",(unsigned long long)done,(unsigned long long)hits,i);fflush(out);return 0;}
  if((i&15)==0)fprintf(stderr,"i=%d done=%llu hits=%llu %.0f/s\n",i,(unsigned long long)done,(unsigned long long)hits,done/el);
 }
finished:
 fflush(out);fclose(out);
 clock_gettime(CLOCK_MONOTONIC,&t1);double el=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)/1e9;
 fprintf(stderr,"DONE done=%llu hits=%llu %.1fs %.0f/s\n",(unsigned long long)done,(unsigned long long)hits,el,done/el);
 return 0;}
