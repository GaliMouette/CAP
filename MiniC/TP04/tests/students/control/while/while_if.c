#include "printlib.h"

int main()
{
    int i;

    i = 1;
    while (i < 10)
    {
        if (i % 2 == 0)
        {
            println_int(i);
        }
        i = i + 1;
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 2
// 4
// 6
// 8
