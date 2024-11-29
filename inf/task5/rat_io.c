#include "rat_io.h"
#include <stdio.h>

void rat_print(rational_t r) {
    if (rat_denom(r) == 1) {
        printf("%lld\n", rat_num(r));  // Используем формат long long
    } else {
        printf("%lld/%llu\n", rat_num(r), rat_denom(r));  // Используем формат long long и unsigned long long
    }
}

rational_t rat_parse(const char *str) {
    long long n;
    unsigned long long d = 1;
    sscanf(str, "%lld/%llu", &n, &d);
    return rational(n, d);
}
