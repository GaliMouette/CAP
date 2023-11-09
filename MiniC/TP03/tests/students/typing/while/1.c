#include "printlib.h"

int main()
{
    bool a;

    while (a)
    {
        a = 1;
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 9 col 8: type mismatch for a: boolean and integer
