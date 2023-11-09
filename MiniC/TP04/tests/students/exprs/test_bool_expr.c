#include "printlib.h"

int main()
{
        int x, y;
        bool a, b;

        a = false;
        b = false;

        println_bool(a == b);
        println_bool(a != b);
        println_bool(a && b);
        println_bool(a || b);

        b = true;

        println_bool(a == b);
        println_bool(a != b);
        println_bool(a && b);
        println_bool(a || b);

        a = true;
        b = false;

        println_bool(a && b);
        println_bool(a || b);

        b = true;

        println_bool(a && b);
        println_bool(a || b);

        println_bool(1 == 1);
        println_bool(1 == 2);
        println_bool(1 != 1);
        println_bool(1 != 2);
        println_bool(1 < 2);
        println_bool(1 < 0);
        println_bool(1 <= 2);
        println_bool(1 <= 0);
        println_bool(1 > 2);
        println_bool(1 > 0);
        println_bool(1 >= 2);
        println_bool(1 >= 0);
        println_bool(!(1 < 2));

        x = 1;
        y = 2;

        println_bool(x == y - 1);
        println_bool(x == y);
        println_bool(x != y - 1);
        println_bool(x != y);
        println_bool(x < y);
        println_bool(x < y - 2);
        println_bool(x <= y);
        println_bool(x <= y - 2);
        println_bool(x > y);
        println_bool(x > y - 2);
        println_bool(x >= y);
        println_bool(x >= y - 2);
        println_bool(!(x < y));

        return 0;
}

// EXPECTED
// 1
// 0
// 0
// 0
// 0
// 1
// 0
// 1
// 0
// 1
// 1
// 1
// 1
// 0
// 0
// 1
// 1
// 0
// 1
// 0
// 0
// 1
// 0
// 1
// 0
// 1
// 0
// 0
// 1
// 1
// 0
// 1
// 0
// 0
// 1
// 0
// 1
// 0
