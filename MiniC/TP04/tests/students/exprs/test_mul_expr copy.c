#include "printlib.h"

int main()
{
    int x;
    x = 8;

    println_int(x * x);
    println_int(x * 2);
    println_int(-2 * x);

    println_int(x / x);
    println_int(x / 2);
    println_int(32 / x);

    println_int(x % x);
    println_int(x % 3);
    println_int(9 % x);
    return 0;
}

// EXPECTED
// 64
// 16
// -16
// 1
// 4
// 4
// 0
// 2
// 1
