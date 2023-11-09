#include "printlib.h"

int main()
{
    int i;
    int j;

    for (i = 1; i < 5; i = i + 1)
    {

        for (j = 1; j <= i; j = j + 1)
        {
            println_int(j);
        }
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
