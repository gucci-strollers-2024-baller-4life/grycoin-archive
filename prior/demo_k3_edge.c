#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "md5mini.h"
static unsigned char buf[4096]; static int n, pos[2048], np;
static inline unsigned char sw(unsigned char c){return (c>=65&&c<=90)?c+32:c-32;}
static inline int isal(unsigned char c){return (c>=65&&c<=90)||(c>=97&&c<=122);}
int main(int argc,char**argv){
  int K=atoi(argv[1]);
  FILE*f=fopen("demo_base.txt","rb"); n=fread(buf,1,sizeof buf,f); fclose(f);
  char *used=calloc(n,1);
  for(int i=0;i<n;i++){ if(isal(buf[i]) && (i==0||!isal(buf[i-1]))) used[i]=1; if(isal(buf[i]) && (i==n-1||!isal(buf[i+1]))) used[i]=1; }
  for(int i=0;i<n;i++) if(used[i]) pos[np++]=i;
  fprintf(stderr,"n=%d edgepos=%d maxk=%d\n",n,np,K);
  long long total=0; int hits=0;
  // nested up to K<=4 via recursion-free loops for K=3 and 4
  if(K==3){
   for(int a=0;a<np-2;a++){ int pa=pos[a];
    mctx pre; minit(&pre); mupdate(&pre,buf,pa); unsigned char fa=sw(buf[pa]); mupdate(&pre,&fa,1);
    for(int b=a+1;b<np-1;b++){ int pb=pos[b];
     mctx A=pre; mupdate(&A,buf+pa+1,pb-pa-1); unsigned char fb=sw(buf[pb]); mupdate(&A,&fb,1);
     for(int c=b+1;c<np;c++){ int pc=pos[c];
      mctx B=A; mupdate(&B,buf+pb+1,pc-pb-1); unsigned char fc=sw(buf[pc]); mupdate(&B,&fc,1);
      mupdate(&B,buf+pc+1,n-pc-1);
      unsigned char d[16]; mfinal(&B,d); total++;
      if(d[0]==0x3c&&(d[1]>>4)==0x6){ printf("HIT3 %d,%d,%d ",pa,pb,pc); for(int i=0;i<16;i++)printf("%02x",d[i]); printf("\n"); fflush(stdout); hits++; }
     } if(b%100==0) fprintf(stderr,"a=%d b=%d total=%lld\n",a,b,total);
    }
   }
  }
  fprintf(stderr,"tested=%lld hits=%d\n",total,hits);
  return 0;
}
