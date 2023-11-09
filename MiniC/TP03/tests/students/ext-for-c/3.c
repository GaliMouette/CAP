#include "printlib.h"

int main()
{
    int i;

    for (i = 2; i < 10;)
    {
        println_int(i);
        i = i + 1;
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 2
// 3
// 4
// 5
// 6
// 7
// 8
// 9
