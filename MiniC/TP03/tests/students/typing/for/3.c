#include "printlib.h"

int main()
{
    int i;

    for (i = 2; i < 10; i = i + 1.5)
    {
        println_int(i);
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 7 col 28: invalid type for additive operands: integer and float
