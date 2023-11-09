#include "printlib.h"

int main()
{
    bool a;

    a = 0.3 || 1;
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 7 col 8: invalid type for or operands: float and integer
