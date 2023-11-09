#include "printlib.h"

int main()
{
    bool b;
    b = false;

    if (b)
    {
        println_int(1);
    }

    b = true;

    if (b)
    {
        println_int(1);
    }

    return 0;
}

// EXPECTED
// EXECCODE 0
// 1
