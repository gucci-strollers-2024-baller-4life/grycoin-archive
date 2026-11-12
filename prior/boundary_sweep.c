#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"

/* usage: boundary_sweep base.txt prefix positions.txt [mask_lo mask_hi]
   enumerates all subsets of positions (toggle case), full rehash, print 3c6-style matches */
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    fseek(f,0,SEEK_END); long l = ftell(f); fseek(f,0,SEEK_SET);
    uint8_t *base = malloc(l); fread(base,1,l,f); fclose(f);
    uint8_t *work = malloc(l); memcpy(work, base, l);
    const char *pre = argv[2];
    int plen = strlen(pre);
    int pos[64]; int n = 0;
    FILE *pf = fopen(argv[3], "r");
    int v; while (n < 64 && fscanf(pf, "%d", &v) == 1) pos[n++] = v;
    fclose(pf);
    fprintf(stderr, "base=%ld bytes, %d positions\n", l, n);
    uint64_t total = 1ULL << n;
    uint64_t lo = (argc > 4) ? strtoull(argv[4],0,10) : 0;
    uint64_t hi = (argc > 5) ? strtoull(argv[5],0,10) : total;
    uint8_t h[16]; char hex[33];
    for (uint64_t mask = lo; mask < hi; mask++) {
        for (int i = 0; i < n; i++) {
            uint8_t c = base[pos[i]];
            work[pos[i]] = (mask >> i & 1) ? (islower(c)?(uint8_t)toupper(c):(uint8_t)tolower(c)) : c;
        }
        md5_digest(work, l, h);
        const char *x = "0123456789abcdef";
        for (int i = 0; i < 16; i++){ hex[2*i]=x[h[i]>>4]; hex[2*i+1]=x[h[i]&15]; }
        hex[32]=0;
        if (!strncmp(hex, pre, plen)) {
            printf("MATCH mask=%llu flips=", (unsigned long long)mask);
            int first=1;
            for (int i = 0; i < n; i++) if (mask>>i&1) { printf("%s%d", first?"":",", pos[i]); first=0; }
            printf(" md5=%s\n", hex); fflush(stdout);
        }
    }
    fprintf(stderr, "done %llu..%llu\n", (unsigned long long)lo, (unsigned long long)hi);
    return 0;
}
