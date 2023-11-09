#include "printlib.h"

int main()
{
    if (1)
    {
        println_bool(true);
    }
    else
    {
        println_bool(false);
    }
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 5 col 4: invalid type for if statement: integer
