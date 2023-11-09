#include "printlib.h"

int main()
{
    bool a;

    if (a)
    {
        a = 1;
    }
    else
    {
        a = true;
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 9 col 8: type mismatch for a: boolean and integer
