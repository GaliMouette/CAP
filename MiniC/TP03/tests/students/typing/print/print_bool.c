#include "printlib.h"

int main()
{
    println_bool("true");
    return 0;
}

// EXPECTED
// EXITCODE 2
// In function main: Line 5 col 4: invalid type for println_bool statement: string
