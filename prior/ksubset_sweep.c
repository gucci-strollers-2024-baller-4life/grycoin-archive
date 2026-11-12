#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"
/* usage: ksubset_sweep base.txt prefix positions.txt kmax [mask_lo mask_hi]
   enumerates all subsets of size 1..kmax of the position pool, prints prefix matches */
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    fseek(f,0,SEEK_END); long l = ftell(f); fseek(f,0,SEEK_SET);
    uint8_t *base = malloc(l); fread(base,1,l,f); fclose(f);
    uint8_t *work = malloc(l); memcpy(work, base, l);
    const char *pre = argv[2]; int plen = strlen(pre);
    int pos[1024]; int n = 0;
    FILE *pf = fopen(argv[3], "r");
    int v; while (n < 1024 && fscanf(pf, "%d", &v) == 1) pos[n++] = v;
    fclose(pf);
    int kmax = atoi(argv[4]);
    fprintf(stderr, "base=%ld bytes, %d positions, kmax=%d\n", l, n, kmax);
    uint8_t h[16]; char hex[33]; const char *x = "0123456789abcdef";
    /* fix first k-1 positions incrementally is complex; simple: enumerate combos via recursion-free loops */
    int idx[8];
    for (int k = 1; k <= kmax && k <= 8; k++) {
        for (int i = 0; i < k; i++) idx[i] = i;
        uint64_t cnt = 0;
        while (1) {
            memcpy(work, base, l);
            for (int i = 0; i < k; i++) {
                int p = pos[idx[i]];
                uint8_t c = base[p];
                work[p] = islower(c) ? (uint8_t)toupper(c) : (uint8_t)tolower(c);
            }
            md5_digest(work, l, h);
            for (int i = 0; i < 16; i++){ hex[2*i]=x[h[i]>>4]; hex[2*i+1]=x[h[i]&15]; }
            hex[32]=0;
            if (!strncmp(hex, pre, plen)) {
                printf("K%d flips=", k);
                for (int i = 0; i < k; i++) printf("%s%d", i?",":"", pos[idx[i]]);
                printf(" md5=%s\n", hex); fflush(stdout);
            }
            cnt++;
            /* next combo */
            int i = k - 1;
            while (i >= 0 && idx[i] == n - k + i) i--;
            if (i < 0) break;
            idx[i]++;
            for (int j = i+1; j < k; j++) idx[j] = idx[j-1]+1;
        }
        fprintf(stderr, "k=%d done: %llu combos\n", k, (unsigned long long)cnt);
    }
    return 0;
}
