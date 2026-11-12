#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"

/* usage: extra_sweep base.txt prefix fixed.txt pool.txt k
   flips fixed positions + all C(pool,k) combinations; prints prefix matches */
static uint8_t *base, *work; static long blen;
static int fixed[64], nfix, pool[2048], npool;
static const char *pre; static int plen;
static long hits = 0;

static void test(void) {
    md5_digest(work, blen, (uint8_t*)work+blen); /* dummy to get type right below */
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1],"rb"); fseek(f,0,SEEK_END); blen=ftell(f); fseek(f,0,SEEK_SET);
    base = malloc(blen+16); work = malloc(blen+16);
    if (fread(base,1,blen,f) != (size_t)blen) return 1; fclose(f);
    pre = argv[2]; plen = strlen(pre);
    FILE *pf = fopen(argv[3],"r"); nfix=0; int v;
    while (nfix<64 && fscanf(pf,"%d",&v)==1) fixed[nfix++]=v; fclose(pf);
    pf = fopen(argv[4],"r"); npool=0;
    while (npool<2048 && fscanf(pf,"%d",&v)==1) pool[npool++]=v; fclose(pf);
    int k = atoi(argv[5]);
    fprintf(stderr,"base=%ld fixed=%d pool=%d k=%d\n", blen, nfix, npool, k);
    uint8_t h[16]; char hex[33]; const char *x="0123456789abcdef";
    int idx[8];
    for (int i=0;i<k;i++) idx[i]=i;
    long long total = 0;
    while (1) {
        memcpy(work, base, blen);
        for (int i=0;i<nfix;i++){ uint8_t c=work[fixed[i]]; work[fixed[i]] = islower(c)?toupper(c):tolower(c); }
        for (int i=0;i<k;i++){ int p=pool[idx[i]]; uint8_t c=work[p]; work[p] = islower(c)?toupper(c):tolower(c); }
        md5_digest(work, blen, h);
        for (int i=0;i<16;i++){ hex[2*i]=x[h[i]>>4]; hex[2*i+1]=x[h[i]&15]; }
        hex[32]=0;
        if (!strncmp(hex, pre, plen)) {
            printf("MATCH extra=");
            for (int i=0;i<k;i++) printf("%s%d", i?",":"", pool[idx[i]]);
            printf(" md5=%s\n", hex); fflush(stdout);
            hits++;
        }
        total++;
        /* next combination */
        int i = k-1;
        while (i>=0 && idx[i]==npool-k+i) i--;
        if (i<0) break;
        idx[i]++;
        for (int j=i+1;j<k;j++) idx[j]=idx[j-1]+1;
    }
    fprintf(stderr,"done k=%d total=%lld hits=%ld\n", k, total, hits);
    return 0;
}
