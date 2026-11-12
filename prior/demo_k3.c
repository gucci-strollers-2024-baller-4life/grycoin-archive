#include <stdio.h>
#include <string.h>
#include <omp.h>
#include "md5mini.h"
static unsigned char buf[4096]; static int n, alpha[2048], na;
static inline unsigned char sw(unsigned char c){return (c>=65&&c<=90)?c+32:c-32;}
static inline int isal(unsigned char c){return (c>=65&&c<=90)||(c>=97&&c<=122);}
int main(void){
  FILE*f=fopen("demo_base.txt","rb"); n=fread(buf,1,sizeof buf,f); fclose(f);
  for(int i=0;i<n;i++) if(isal(buf[i])) alpha[na++]=i;
  fprintf(stderr,"n=%d alpha=%d triples=%lld\n",n,na,(long long)na*(na-1)*(na-2)/6);
  long long total=0; int hits=0;
  #pragma omp parallel for schedule(dynamic,4) reduction(+:total,hits)
  for(int a=0;a<na-2;a++){
    int pa=alpha[a];
    mctx pre; minit(&pre); mupdate(&pre,buf,pa);
    unsigned char fa=sw(buf[pa]); mupdate(&pre,&fa,1);
    for(int b=a+1;b<na-1;b++){
      int pb=alpha[b];
      mctx A=pre;
      mupdate(&A,buf+pa+1,pb-pa-1);
      unsigned char fb=sw(buf[pb]); mupdate(&A,&fb,1);
      for(int c=b+1;c<na;c++){
        int pc=alpha[c];
        mctx B=A;
        mupdate(&B,buf+pb+1,pc-pb-1);
        unsigned char fc=sw(buf[pc]); mupdate(&B,&fc,1);
        mupdate(&B,buf+pc+1,n-pc-1);
        unsigned char d[16]; mfinal(&B,d);
        total++;
        if(d[0]==0x3c && (d[1]>>4)==0x6){
          #pragma omp critical
          { printf("HIT %d,%d,%d ",pa,pb,pc); for(int i=0;i<16;i++)printf("%02x",d[i]); printf("\n"); fflush(stdout); }
          hits++;
        }
      }
    }
  }
  fprintf(stderr,"tested=%lld hits=%d\n",total,hits);
  return 0;
}
