#include <stdio.h>
int sos(int n){ int s=0,i; for(i=1;i<=n;i++) s+=i*i; return s; }
int main(void){ printf("%d\n", sos(4)); return 0; }
