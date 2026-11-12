/* flipk4 base.txt prefix positions.txt shard nshards -> 4-flip enumeration over supplied positions */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"rb"); fseek(f,0,SEEK_END); long L=ftell(f); fseek(f,0,SEEK_SET);
    uint8_t*base=malloc(L); if(fread(base,1,L,f)!=(size_t)L) return 1; fclose(f);
    const char*pre=argv[2];
    FILE*g=fopen(argv[3],"r"); int*pos=malloc(sizeof(int)*(L+16)); int n=0;
    while(fscanf(g,"%d",&pos[n])==1) n++; fclose(g);
    int shard=atoi(argv[4]), ns=atoi(argv[5]);
    uint8_t*w=malloc(L); memcpy(w,base,L); uint8_t h[16]; char hex[33];
    for(int a=shard;a<n;a+=ns){
        w[pos[a]]^=0x20;
        for(int b=a+1;b<n;b++){
            w[pos[b]]^=0x20;
            for(int c=b+1;c<n;c++){
                w[pos[c]]^=0x20;
                for(int d=c+1;d<n;d++){
                    w[pos[d]]^=0x20;
                    md5_digest(w,L,h);
                    hex[0]=0; for(int i=0;i<16;i++) sprintf(hex+2*i,"%02x",h[i]);
                    if(strlen(pre)==0||!strncmp(hex,pre,strlen(pre))) printf("flips=%d,%d,%d,%d md5=%s\n",a,b,c,d,hex);
                    w[pos[d]]^=0x20;
                }
                w[pos[c]]^=0x20;
            }
            w[pos[b]]^=0x20;
        }
        w[pos[a]]^=0x20;
    }
    return 0;
}
