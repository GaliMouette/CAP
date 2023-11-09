#include "printlib.h"

int main()
{
    int i;

    for (i = 2; i < 10.0; i = i + 1)
    {
        println_int(i);
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 7 col 16: invalid type for relational operands: integer and float
