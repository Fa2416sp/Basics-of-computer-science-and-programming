#include "rational.h"
#include <stdio.h>

void rat_print(rational_t r) {
    if (rat_denom(r) == 1) {
        printf("%ld\n", rat_num(r));
    } else {
        printf("%ld/%u\n", rat_num(r), rat_denom(r));
    }
}

rational_t rat_parse(const char *str) {
    long n, d = 1;
    sscanf(str, "%ld/%ld", &n, &d);
    return rational(n, d);
}
