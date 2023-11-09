#include "printlib.h"

int main()
{
    println_int(3.0 % 2.0);
    return 0;
}

// SKIP TEST EXPECTED
// EXPECTED
// EXITCODE 2
// In function main: Line 5 col 16: invalid type for multiplicative operands: float and float
