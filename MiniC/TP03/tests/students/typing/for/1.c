#include "printlib.h"

int main()
{
    int i;

    for (i = 2.1; i < 10; i = i + 1)
    {
        println_int(i);
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 7 col 9: type mismatch for i: integer and float
