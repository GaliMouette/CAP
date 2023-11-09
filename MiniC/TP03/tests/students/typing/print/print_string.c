#include "printlib.h"

int main()
{
    println_string(true);
    return 0;
}

// EXPECTED
// EXECCODE 0
// EXITCODE 2
// In function main: Line 5 col 4: invalid type for println_string statement: boolean
