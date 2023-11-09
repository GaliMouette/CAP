#include "printlib.h"

int main()
{
    bool b;
    b = false;

    if (b)
    {
        println_int(1);
    }
    else
    {
        println_int(0);
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 0
