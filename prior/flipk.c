/* flipk base.txt prefix k shard nshards  -> prints "flips=i,j,k md5=hex" for hits */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"rb"); if(!f){perror("base");return 1;}
    fseek(f,0,SEEK_END); long L=ftell(f); fseek(f,0,SEEK_SET);
    uint8_t*base=malloc(L); if(fread(base,1,L,f)!=(size_t)L){return 1;} fclose(f);
    const char*pre=argv[2]; int K=atoi(argv[3]); int shard=atoi(argv[4]), ns=atoi(argv[5]);
    int*pos=malloc(sizeof(int)*L); int n=0;
    for(long i=0;i<L;i++) if(isalpha(base[i])) pos[n++]=(int)i;
    uint8_t*w=malloc(L); memcpy(w,base,L);
    uint8_t h[16];
    for(int a=shard;a<n;a+=ns){
        w[pos[a]]^=0x20;
        for(int b=a+1;b<n;b++){
            w[pos[b]]^=0x20;
            if(K==2){
                md5_digest(w,L,h);
                char hex[33]; for(int i=0;i<16;i++) sprintf(hex+2*i,"%02x",h[i]);
                if(!strncmp(hex,pre,strlen(pre))) printf("flips=%d,%d md5=%s\n",a,b,hex);
            } else {
                for(int c=b+1;c<n;c++){
                    w[pos[c]]^=0x20;
                    md5_digest(w,L,h);
                    char hex[33]; for(int i=0;i<16;i++) sprintf(hex+2*i,"%02x",h[i]);
                    if(!strncmp(hex,pre,strlen(pre))) printf("flips=%d,%d,%d md5=%s\n",a,b,c,hex);
                    w[pos[c]]^=0x20;
                }
            }
            w[pos[b]]^=0x20;
        }
        w[pos[a]]^=0x20;
    }
    return 0;
}
