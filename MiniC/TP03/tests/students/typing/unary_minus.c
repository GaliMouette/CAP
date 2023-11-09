#include "printlib.h"

int main()
{
    println_bool(-true);
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 5 col 17: invalid type for unary minus operand: boolean
