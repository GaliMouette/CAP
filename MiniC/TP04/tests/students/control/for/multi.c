#include "printlib.h"

int main()
{
    int i;

    i = 1;
    for (i = 1; i < 10; i = i + 1)
    {
        println_int(i);
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
// 7
// 8
// 9
