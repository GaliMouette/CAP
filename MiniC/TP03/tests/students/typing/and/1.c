#include "printlib.h"

int main()
{
    bool a;

    a = true && 1;
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 7 col 8: invalid type for and operands: boolean and integer
