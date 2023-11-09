#include "printlib.h"

int main()
{
    println_float(1.0 / 0.0);
    return 0;
}

// SKIP TEST EXPECTED
// EXPECTED
// EXECCODE 1
// Division by 0
