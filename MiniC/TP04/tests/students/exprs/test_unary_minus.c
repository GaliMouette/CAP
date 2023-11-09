#include "printlib.h"

int main()
{
    int x, y;
    x = 42;
    y = -x;
    println_int(-x);
    println_int(-y);
    println_int(-1);
    return 0;
}

// EXPECTED
// -42
// 42
// -1
