/*
 * enum_md5.c — exhaustive case-flip enumerator with MD5 prefix oracle.
 *
 * Modes:
 *   one     : all single-letter case flips
 *   two     : all ordered pairs of distinct letter case flips
 *   sentmask: all subsets of a supplied positions file (2^k masks)
 *   oneat   : single flips only at positions from a positions file
 *   twoat   : pairs of flips both drawn from a positions file
 *
 * Usage:
 *   ./enum_md5 <base.txt> <hexprefix> <mode> [positions.txt]
 *
 * "Flip" = toggle the case of an ASCII letter (a<->A).
 * Base file is hashed with NO trailing newline added: exact bytes as given.
 * Matches print: MODE, flipped indices, full md5 hex.
 * Positions file (optional): one integer index per line (0-based byte offset).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

/* ---------- compact MD5 ---------- */
typedef struct {
    uint32_t s[4];
    uint64_t bits;
    uint8_t  buf[64];
    size_t   blen;
} MD5;

static const uint32_t K[64] = {
    0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
    0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
    0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
    0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
    0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
    0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
    0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
    0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391
};
static const int R[64] = {
    7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
    5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
    4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
    6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21
};

#define ROTL(x,c) (((x)<<(c))|((x)>>(32-(c))))

static void md5_block(uint32_t *s, const uint8_t *p) {
    uint32_t a=s[0],b=s[1],c=s[2],d=s[3],m[16],f,g,t;
    for (int i=0;i<16;i++)
        m[i] = p[4*i] | (p[4*i+1]<<8) | (p[4*i+2]<<16) | ((uint32_t)p[4*i+3]<<24);
    for (int i=0;i<64;i++) {
        if (i<16)      { f=(b&c)|(~b&d); g=i; }
        else if (i<32) { f=(d&b)|(~d&c); g=(5*i+1)&15; }
        else if (i<48) { f=b^c^d;        g=(3*i+5)&15; }
        else           { f=c^(b|~d);     g=(7*i)&15; }
        t = d; d = c; c = b;
        b = b + ROTL(a + f + K[i] + m[g], R[i]);
        a = t;
    }
    s[0]+=a; s[1]+=b; s[2]+=c; s[3]+=d;
}

static void md5_init(MD5 *m){ m->s[0]=0x67452301;m->s[1]=0xefcdab89;m->s[2]=0x98badcfe;m->s[3]=0x10325476;m->bits=0;m->blen=0; }
static void md5_update(MD5 *m, const uint8_t *p, size_t n) {
    m->bits += (uint64_t)n << 3;
    while (n) {
        size_t take = 64 - m->blen; if (take > n) take = n;
        memcpy(m->buf + m->blen, p, take);
        m->blen += take; p += take; n -= take;
        if (m->blen == 64) { md5_block(m->s, m->buf); m->blen = 0; }
    }
}
static void md5_digest(const uint8_t *p, size_t n, uint8_t out[16]) {
    MD5 m; md5_init(&m); md5_update(&m, p, n);
    uint64_t bits = (uint64_t)n << 3;
    uint8_t fin[128]; size_t fl = 0;
    fin[fl++] = 0x80;
    size_t r = n & 63;
    size_t pl = (r < 56) ? (56 - r - 1) : (120 - r - 1);
    while (fl < pl + 1) fin[fl++] = 0;
    for (int i = 0; i < 8; i++) fin[fl++] = (uint8_t)(bits >> (8*i));
    md5_update(&m, fin, fl);
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            out[4*i+j] = (uint8_t)(m.s[i] >> (8*j));
}
/* ---------- end MD5 ---------- */

static uint8_t *g_buf; static size_t g_len;
static uint8_t g_work[1<<20]; /* working copy (base text must be < 1MB) */
static uint8_t g_hash[16];
static char g_pre[64]; static int g_prelen; /* target prefix hex chars */

static void hex(const uint8_t h[16], char *out) {
    const char *x = "0123456789abcdef";
    for (int i=0;i<16;i++){ out[2*i]=x[h[i]>>4]; out[2*i+1]=x[h[i]&15]; }
    out[32]=0;
}
static int prefix_ok(const uint8_t h[16]) {
    char s[33]; hex(h,s);
    return strncmp(s, g_pre, g_prelen) == 0;
}
static void try_candidate(const char *mode, const int *flips, int nflips) {
    for (int i=0;i<nflips;i++) {
        uint8_t c = g_buf[flips[i]];
        g_work[flips[i]] = islower(c) ? (uint8_t)toupper(c) : (uint8_t)tolower(c);
    }
    md5_digest(g_work, g_len, g_hash);
    if (prefix_ok(g_hash)) {
        char s[33]; hex(g_hash,s);
        printf("MATCH %s flips=", mode);
        for (int i=0;i<nflips;i++) printf("%d%s", flips[i], i+1<nflips?"," : "");
        printf(" md5=%s\n", s); fflush(stdout);
    }
    for (int i=0;i<nflips;i++) g_work[flips[i]] = g_buf[flips[i]];
}

static int isposanchor(int p, int *a, int n){ for(int i=0;i<n;i++) if(a[i]==p) return 1; return 0; }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s base.txt hexprefix mode [positions.txt]\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("open base"); return 1; }
    fseek(f, 0, SEEK_END); long l = ftell(f); fseek(f, 0, SEEK_SET);
    g_buf = malloc(l); g_len = l;
    if (fread(g_buf, 1, l, f) != (size_t)l) { perror("read"); return 1; }
    fclose(f);
    memcpy(g_work, g_buf, g_len);
    snprintf(g_pre, sizeof g_pre, "%s", argv[2]);
    g_prelen = strlen(g_pre);
    const char *mode = argv[3];

    /* sanity: print base hash */
    md5_digest(g_buf, g_len, g_hash);
    char b[33]; hex(g_hash, b);
    fprintf(stderr, "base md5 = %s (len=%zu)\n", b, g_len);

    /* letter positions */
    int *pos = malloc(g_len * sizeof(int)); int npos = 0;
    for (size_t i=0;i<g_len;i++) if (isalpha(g_buf[i])) pos[npos++] = (int)i;

    /* optional positions file */
    int *ppos = NULL; int nppos = 0;
    if (argc > 4) {
        FILE *pf = fopen(argv[4], "r");
        if (!pf) { perror("open positions"); return 1; }
        ppos = malloc(g_len * sizeof(int)); int v;
        while (fscanf(pf, "%d", &v) == 1) ppos[nppos++] = v;
        fclose(pf);
        fprintf(stderr, "positions file: %d indices\n", nppos);
    }

    if (!strcmp(mode, "one")) {
        int fl[1];
        for (int i=0;i<npos;i++){ fl[0]=pos[i]; try_candidate("one",fl,1); }
    } else if (!strcmp(mode, "two")) {
        int fl[2];
        for (int i=0;i<npos;i++) for (int j=i+1;j<npos;j++){
            fl[0]=pos[i]; fl[1]=pos[j]; try_candidate("two",fl,2);
        }
    } else if (!strcmp(mode, "sentmask")) {
        if (!nppos) { fprintf(stderr,"sentmask needs positions file\n"); return 2; }
        int k = nppos; if (k > 20) { fprintf(stderr,"too many sentences (%d), cap 20\n", k); return 2; }
        int fl[20];
        for (unsigned mask=0; mask < (1u<<k); mask++) {
            int n=0;
            for (int i=0;i<k;i++) if (mask & (1u<<i)) fl[n++]=ppos[i];
            if (n) try_candidate("sentmask",fl,n); /* mask 0 = base text, skipped */
        }
    } else if (!strcmp(mode, "oneat")) {
        int fl[1];
        for (int i=0;i<nppos;i++){ fl[0]=ppos[i]; try_candidate("oneat",fl,1); }
    } else if (!strcmp(mode, "twoat")) {
        int fl[2];
        for (int i=0;i<nppos;i++) for (int j=i+1;j<nppos;j++){
            fl[0]=ppos[i]; fl[1]=ppos[j]; try_candidate("twoat",fl,2);
        }

    } else if (!strcmp(mode, "three")) {
        int fl[3];
        for (int i=0;i<npos;i++) for (int j=i+1;j<npos;j++) for (int k2=j+1;k2<npos;k2++){
            fl[0]=pos[i]; fl[1]=pos[j]; fl[2]=pos[k2]; try_candidate("three",fl,3);
        }
    } else if (!strcmp(mode, "anchor")) {
        /* anchors file = positions always toggled; argv[4] = extra count k */
        int k = argc > 4 ? atoi(argv[4]) : 2;
        if (!nppos || nppos % 2) { fprintf(stderr,"anchor file needs pairs\n"); return 2; }
        int na = nppos;
        int anchors[8]; for (int i=0;i<na;i++) anchors[i]=ppos[i];
        memcpy(g_work, g_buf, g_len);
        for (int i=0;i<na;i++) { uint8_t c=g_work[anchors[i]]; g_work[anchors[i]] = islower(c)?(uint8_t)toupper(c):(uint8_t)tolower(c); }
        int fl[8];
        if (k==1) {
            for (int i=0;i<npos;i++) { if (isposanchor(pos[i],anchors,na)) continue; fl[0]=pos[i]; try_candidate("anchor",fl,1); }
        } else if (k==2) {
            for (int i=0;i<npos;i++) { if (isposanchor(pos[i],anchors,na)) continue;
                for (int j=i+1;j<npos;j++) { if (isposanchor(pos[j],anchors,na)) continue;
                    fl[0]=pos[i]; fl[1]=pos[j]; try_candidate("anchor",fl,2); } }
        } else if (k==3) {
            for (int i=0;i<npos;i++) { if (isposanchor(pos[i],anchors,na)) continue;
                for (int j=i+1;j<npos;j++) { if (isposanchor(pos[j],anchors,na)) continue;
                    for (int j2=j+1;j2<npos;j2++) { if (isposanchor(pos[j2],anchors,na)) continue;
                        fl[0]=pos[i]; fl[1]=pos[j]; fl[2]=pos[j2]; try_candidate("anchor",fl,3); } } }
        }
    } else if (!strcmp(mode, "unitmask")) {
        if (!nppos) { fprintf(stderr,"unitmask needs positions file (2 ints per line)\n"); return 2; }
        int k = nppos / 2; if (nppos % 2) { fprintf(stderr,"positions file needs even count\n"); return 2; }
        if (k > 24) { fprintf(stderr,"too many units (%d), cap 24\n", k); return 2; }
        int fl[48];
        for (unsigned mask = 0; mask < (1u << k); mask++) {
            int n = 0;
            for (int i = 0; i < k; i++) if (mask & (1u << i)) {
                int fi = ppos[2*i], li = ppos[2*i+1];
                if (fi >= 0) fl[n++] = fi;
                if (li >= 0) fl[n++] = li;
            }
            /* directional: first-indexed -> tolower if upper; last-indexed -> toupper if lower */
            int applied[48]; int na = 0;
            for (int i = 0; i < k; i++) if (mask & (1u << i)) {
                int fi = ppos[2*i], li = ppos[2*i+1];
                if (fi >= 0 && isupper(g_buf[fi])) { g_work[fi] = (uint8_t)tolower(g_buf[fi]); applied[na++] = fi; }
                if (li >= 0 && islower(g_buf[li])) { g_work[li] = (uint8_t)toupper(g_buf[li]); applied[na++] = li; }
            }
            if (na) {
                md5_digest(g_work, g_len, g_hash);
                if (prefix_ok(g_hash)) {
                    char hs[33]; hex(g_hash, hs);
                    printf("MATCH unitmask mask=%u flips=", mask);
                    for (int i = 0; i < na; i++) printf("%d%s", applied[i], i+1<na ? "," : "");
                    printf(" md5=%s\n", hs); fflush(stdout);
                }
            }
            for (int i = 0; i < na; i++) g_work[applied[i]] = g_buf[applied[i]];
        }
    } else {
        fprintf(stderr, "unknown mode %s\n", mode); return 2;
    }
    fprintf(stderr, "done.\n");
    return 0;
}
