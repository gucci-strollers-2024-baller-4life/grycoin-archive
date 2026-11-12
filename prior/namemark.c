/* namemark base.txt prefix NAME -> enumerate in-order case-uppercase markings of NAME in base;
   print md5s with given hex prefix, plus stderr progress/count */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include "md5_core.h"

static uint8_t *buf; static long L; static const char *name; static int NL;
static int **pos; static int *cnt; static long long tested=0, hits=0;
static const char *prefix; static int PL;
static struct timespec t0;

static double elapsed(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return (t.tv_sec-t0.tv_sec)+(t.tv_nsec-t0.tv_nsec)/1e9; }

static void rec(int k,int start){
    if(k==NL){
        uint8_t h[16]; md5_digest(buf,L,h);
        char hex[33]; for(int i=0;i<16;i++) sprintf(hex+2*i,"%02x",h[i]);
        tested++;
        if(!strncmp(hex,prefix,PL)){ hits++; printf("md5=%s\n",hex); fflush(stdout); }
        if((tested&0xFFFFF)==0) fprintf(stderr,"\r%d/%d tested=%lld hits=%lld %.0fs",k,NL,tested,hits,elapsed());
        return;
    }
    for(int j=0;j<cnt[k];j++){
        int p=pos[k][j];
        if(p<start) continue;
        uint8_t old=buf[p];
        buf[p]=(uint8_t)toupper(old);
        rec(k+1,p+1);
        buf[p]=old;
    }
}

int main(int argc,char**argv){
    clock_gettime(CLOCK_MONOTONIC,&t0);
    FILE*f=fopen(argv[1],"rb"); if(!f){perror("base");return 1;}
    fseek(f,0,SEEK_END); L=ftell(f); fseek(f,0,SEEK_SET);
    buf=malloc(L); if(fread(buf,1,L,f)!=(size_t)L) return 1; fclose(f);
    prefix=argv[2]; PL=strlen(prefix); name=argv[3]; NL=strlen(name);
    pos=malloc(sizeof(int*)*NL); cnt=calloc(NL,sizeof(int));
    for(int k=0;k<NL;k++){
        cnt[k]=0;
        for(long i=0;i<L;i++) if(islower(buf[i]) && buf[i]==(uint8_t)tolower(name[k])) cnt[k]++;
        pos[k]=malloc(sizeof(int)*cnt[k]);
        int n=0;
        for(long i=0;i<L;i++) if(islower(buf[i]) && buf[i]==(uint8_t)tolower(name[k])) pos[k][n++]=i;
    }
    fprintf(stderr,"positions per letter:"); for(int k=0;k<NL;k++) fprintf(stderr," %d",cnt[k]); fprintf(stderr,"\n");
    rec(0,0);
    fprintf(stderr,"\nDONE name=%s tested=%lld hits=%lld %.1fs\n",name,tested,hits,elapsed());
    return 0;
}
