#include "printlib.h"

int main()
{
    bool a;

    a = "true" && false;
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 7 col 8: invalid type for and operands: string and boolean
