#include "printlib.h"

int main()
{
    bool b;
    int i;

    b = true;
    i = 1;

    if (b)
    {
        while (i < 4)
        {
            println_int(i);
            i = i + 1;
        }
    }
    else
    {
        println_int(0);
    }

    b = false;

    if (b)
    {
        println_int(0);
    }
    else
    {
        while (i < 7)
        {
            println_int(i);
            i = i + 1;
        }
    }

    return 0;
}

// EXPECTED
// EXECCODE 0
// 1
// 2
// 3
// 4
// 5
// 6
