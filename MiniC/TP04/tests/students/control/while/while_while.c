#include "printlib.h"

int main()
{
    int i;
    int j;

    i = 1;
    while (i < 5)
    {
        j = 1;
        while (j <= i)
        {
            println_int(j);
            j = j + 1;
        }
        i = i + 1;
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 1
// 1
// 2
// 1
// 2
// 3
// 1
// 2
// 3
// 4
