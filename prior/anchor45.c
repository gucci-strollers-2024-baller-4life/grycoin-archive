#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"
/* anchored sweep: base with stated pair applied (I535->i, f652->F) + k extra alpha flips
   usage: anchor45 base2.txt prefix kmax */
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    fseek(f,0,SEEK_END); long l = ftell(f); fseek(f,0,SEEK_SET);
    uint8_t *base = malloc(l); fread(base,1,l,f); fclose(f);
    const char *pre = argv[2];
    int kmax = atoi(argv[3]);
    int pos[2048]; int n = 0;
    for (long i = 0; i < l; i++)
        if (isalpha(base[i])) { pos[n] = i; n++; }
    fprintf(stderr, "base=%ld bytes, %d alpha positions\n", l, n);
    uint8_t *work = malloc(l);
    uint8_t h[16]; char hex[33];
    const char *x = "0123456789abcdef";
    /* k = kmax only (k< done previously) */
    if (kmax == 3) {
        for (int a = 0; a < n; a++) for (int b = a+1; b < n; b++) for (int c = b+1; c < n; c++) {
            memcpy(work, base, l);
            work[pos[a]] ^= 0x20; work[pos[b]] ^= 0x20; work[pos[c]] ^= 0x20;
            md5_digest(work, l, h);
            sprintf(hex, "%02x%02x%02x", h[0],h[1],h[2]);
            if (strncmp(hex, pre, 3) == 0) {
                char full[33];
                for (int i = 0; i < 16; i++) sprintf(full+i*2, "%02x", h[i]);
                printf("A3 flips=%d,%d,%d md5=%s\n", pos[a], pos[b], pos[c], full);
                fflush(stdout);
            }
        }
        fprintf(stderr, "k=3 done\n");
    } else if (kmax == 4) {
        long total = (long)n*(n-1)*(n-2)*(n-3)/24; long done = 0;
        for (int a = 0; a < n; a++) {
            for (int b = a+1; b < n; b++) for (int c = b+1; c < n; c++) for (int d = c+1; d < n; d++) {
                memcpy(work, base, l);
                work[pos[a]] ^= 0x20; work[pos[b]] ^= 0x20; work[pos[c]] ^= 0x20; work[pos[d]] ^= 0x20;
                md5_digest(work, l, h);
                char hex3[4]; sprintf(hex3, "%02x%02x%02x", h[0],h[1],h[2]);
                if (hex3[0]==pre[0] && hex3[1]==pre[1] && hex3[2]==pre[2]) {
                    char full[33];
                    for (int i = 0; i < 16; i++) sprintf(full+i*2, "%02x", h[i]);
                    printf("A4 flips=%d,%d,%d,%d md5=%s\n", pos[a],pos[b],pos[c],pos[d], full);
                    fflush(stdout);
                }
            }
            done += (long)(n-a-1)*(n-a-2)*(n-a-3)/6;
            if (a % 100 == 0) fprintf(stderr, "a=%d/%d (%.1f%%)\n", a, n, 100.0*done/total);
        }
        fprintf(stderr, "k=4 done\n");
    }
    return 0;
}
