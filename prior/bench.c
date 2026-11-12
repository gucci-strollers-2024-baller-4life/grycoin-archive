#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include "md5_core.h"
int main(int argc, char **argv){
    FILE *f = fopen(argv[1], "rb");
    fseek(f,0,SEEK_END); long l = ftell(f); fseek(f,0,SEEK_SET);
    uint8_t *buf = malloc(l); fread(buf,1,l,f); fclose(f);
    uint8_t out[16];
    for (int i=0;i<10000;i++) md5_digest(buf,l,out);
    clock_t t0 = clock();
    long N = 2000000;
    for (long i=0;i<N;i++) md5_digest(buf,l,out);
    double dt = (double)(clock()-t0)/CLOCKS_PER_SEC;
    printf("%.0f hashes/s (%.1f MB/s), len=%ld\n", N/dt, (double)N*l/dt/1e6, l);
    return 0;
}
