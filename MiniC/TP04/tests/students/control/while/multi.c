#include "printlib.h"

int main()
{
    int i;

    i = 1;
    while (i < 10)
    {
        println_int(i);
        i = i + 1;
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
