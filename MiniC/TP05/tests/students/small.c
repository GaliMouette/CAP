#include "printlib.h"

int main()
{
    int a, b;

    a = 1;
    b = 2;
    if (a == 1 && b == 2)
        println_int(a + b);
    else
        println_int(0);

    return 0;
}

// EXPECTED
// 3
