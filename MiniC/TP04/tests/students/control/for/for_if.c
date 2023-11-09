#include "printlib.h"

int main()
{
    int i;

    i = 1;
    for (i = 1; i < 10; i = i + 1)
    {
        if (i % 2 == 0)
        {
            println_int(i);
        }
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 2
// 4
// 6
// 8
