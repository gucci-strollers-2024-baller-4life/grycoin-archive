#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "md5_core.h"
/* usage: anchor4 base2.txt prefix lo hi  (ranges over first position index) */
int main(int argc, char **argv){
    FILE *f=fopen(argv[1],"rb"); fseek(f,0,SEEK_END); long l=ftell(f); fseek(f,0,SEEK_SET);
    uint8_t *base=malloc(l); fread(base,1,l,f); fclose(f);
    int pos[1400]; int n=0;
    for(long i=0;i<l;i++) if(isalpha(base[i])) pos[n++]=i;
    const char*pre=argv[2];
    int lo=atoi(argv[3]), hi=atoi(argv[4]);
    uint8_t *work=malloc(l); memcpy(work,base,l);
    uint8_t h[16]; char hex[33]; const char*x="0123456789abcdef";
    for(int a=lo;a<hi;a++){
        work[pos[a]] ^= 0x20;
        for(int b=a+1;b<n;b++){
            work[pos[b]] ^= 0x20;
            for(int c=b+1;c<n;c++){
                work[pos[c]] ^= 0x20;
                for(int d=c+1;d<n;d++){
                    work[pos[d]] ^= 0x20;
                    md5_digest(work,l,h);
                    if((h[0]==(uint8_t)pre[0]&&(h[1]>>4))==(uint8_t)(pre[1]|0x20)-87||0){}
                    // hex prefix compare, generic:
                    int ok=1;
                    for(int i=0;i<3;i++){
                        uint8_t nib=(i%2==0)?(h[i/2]>>4):(h[i/2]&0xf);
                        char hx=x[nib]; if(hx!=pre[i]){ok=0;break;}
                    }
                    if(ok){
                        for(int i=0;i<16;i++){hex[i*2]=x[h[i]>>4];hex[i*2+1]=x[h[i]&0xf];}
                        hex[32]=0;
                        printf("K4 pos=%d,%d,%d,%d md5=%s\n",pos[a],pos[b],pos[c],pos[d],hex);
                        fflush(stdout);
                    }
                    work[pos[d]] ^= 0x20;
                }
                work[pos[c]] ^= 0x20;
            }
            work[pos[b]] ^= 0x20;
        }
        work[pos[a]] ^= 0x20;
        fprintf(stderr,"a=%d/%d\n",a,hi); 
    }
    return 0;
}
