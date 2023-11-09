#include "printlib.h"

int main()
{
    int i;

    i = 1;
    while (i <= 1)
    {
        println_int(i);
        i = i + 1;
    }
    return 0;
}

// EXPECTED
// EXECCODE 0
// 1
