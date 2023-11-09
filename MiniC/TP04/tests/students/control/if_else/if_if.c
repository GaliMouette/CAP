#include "printlib.h"

int main()
{
    bool b;
    b = false;

    if (!b)
    {
        if (b)
        {
            println_int(-1);
        }
        else
        {
            println_int(1);
        }
    }
    if (b)
    {
        println_int(-2);
    }
    else
    {
        if (!b)
        {
            println_int(2);
        }
        else
        {
            println_int(-3);
        }
    }

    return 0;
}

// EXPECTED
// EXECCODE 0
// 1
// 2
