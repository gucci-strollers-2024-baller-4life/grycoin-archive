#ifndef MD5MINI_H
#define MD5MINI_H
#include <stdint.h>
#include <string.h>
typedef struct { uint32_t s[4]; uint64_t len; unsigned char blk[64]; uint32_t bl; } mctx;
static const uint32_t MK[64]={
0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391};
static const int MS[64]={7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21};
static inline uint32_t ROT(uint32_t x,int c){return (x<<c)|(x>>(32-c));}
static void mblock(mctx*m,const unsigned char*p){
    uint32_t w[16];
    for(int i=0;i<16;i++) w[i]=p[i*4]|(p[i*4+1]<<8)|(p[i*4+2]<<16)|((uint32_t)p[i*4+3]<<24);
    uint32_t a=m->s[0],b=m->s[1],c=m->s[2],d=m->s[3];
    for(int i=0;i<64;i++){
        uint32_t f; int g;
        if(i<16){f=(b&c)|(~b&d);g=i;}
        else if(i<32){f=(d&b)|(~d&c);g=(5*i+1)&15;}
        else if(i<48){f=b^c^d;g=(3*i+5)&15;}
        else {f=c^(b|~d);g=(7*i)&15;}
        uint32_t t=d; d=c; c=b;
        b=b+ROT(a+f+MK[i]+w[g],MS[i]);
        a=t;
    }
    m->s[0]+=a;m->s[1]+=b;m->s[2]+=c;m->s[3]+=d;
}
static inline void minit(mctx*m){m->s[0]=0x67452301;m->s[1]=0xefcdab89;m->s[2]=0x98badcfe;m->s[3]=0x10325476;m->len=0;m->bl=0;}
static inline void mupdate(mctx*m,const unsigned char*p,size_t n){
    m->len+=n;
    while(n){
        size_t k=64-m->bl; if(k>n)k=n;
        memcpy(m->blk+m->bl,p,k); m->bl+=k; p+=k; n-=k;
        if(m->bl==64){ mblock(m,m->blk); m->bl=0; }
    }
}
static inline void mfinal(mctx*m,unsigned char out[16]){
    uint64_t bits=m->len*8;
    unsigned char pad=0x80; mupdate(m,&pad,1);
    unsigned char z=0; while(m->bl!=56) mupdate(m,&z,1);
    unsigned char lb[8]; for(int i=0;i<8;i++) lb[i]=(bits>>(8*i))&0xff;
    m->len-=0; mupdate(m,lb,8);
    for(int i=0;i<4;i++){out[i*4]=m->s[i]&0xff;out[i*4+1]=(m->s[i]>>8)&0xff;out[i*4+2]=(m->s[i]>>16)&0xff;out[i*4+3]=(m->s[i]>>24)&0xff;}
}
#endif
