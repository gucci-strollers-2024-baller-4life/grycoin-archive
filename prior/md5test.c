#include <stdio.h>
#include "md5mini.h"
int main(void){FILE*f=fopen("demo_base.txt","rb");unsigned char b[4096];size_t n=fread(b,1,sizeof b,f);fclose(f);
mctx m;minit(&m);mupdate(&m,b,n);unsigned char d[16];mfinal(&m,d);
for(int i=0;i<16;i++)printf("%02x",d[i]);printf("\n");return 0;}
