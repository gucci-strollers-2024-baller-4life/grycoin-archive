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
