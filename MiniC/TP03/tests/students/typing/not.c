#include "printlib.h"

int main()
{
    println_bool(!"true");
    return 0;
}

// SKIP TEST EXPECTED
// EXPECTED
// EXITCODE 2
// In function main: Line 5 col 17: invalid type for not operand: string
