#include "printlib.h"

int main()
{
    bool a;

    if (!a)
    {
        a = true;
    }
    else
    {
        a = 1;
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 13 col 8: type mismatch for a: boolean and integer
