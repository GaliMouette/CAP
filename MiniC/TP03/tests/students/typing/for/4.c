#include "printlib.h"

int main()
{
    int i;

    for (i = 2; i < 10; i = i + 1)
    {
        println_int(i + true);
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 9 col 20: invalid type for additive operands: integer and boolean
