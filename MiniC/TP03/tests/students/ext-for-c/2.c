#include "printlib.h"

int main()
{
    float i;

    i = 1.0;
    for (; i < 9.9; i = i + 1.15)
    {
        println_float(i);
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 1.00
// 2.15
// 3.30
// 4.45
// 5.60
// 6.75
// 7.90
// 9.05
