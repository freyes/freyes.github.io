Title: C Snippets
Date: 2013-01-01
Category: Snippets

## Simple Swap Function

```C
#include <stdio.h>

inline void swap(int *a, int *b){
  *a= *a+*b;
  *b=*a-*b;
  *a=*a-*b;
}

int main() {
  int a = 1;
  int b = 2;

  printf("before: a: %d - b: %d\n", a, b);
  swap(&a, &b);

  printf("after: a: %d - b: %d\n", a, b);
  return 0;
}
```

Expected output:

```
before: a: 1 - b: 2
after: a: 2 - b: 1
```
