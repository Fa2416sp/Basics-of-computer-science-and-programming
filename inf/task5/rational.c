#include "rational.h"
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

static long long gcd(long long a, long long b) {
    while (b != 0) {
        long long t = b;
        b = a % b;
        a = t;
    }
    return a;
}

rational_t rational(long long n, unsigned long long d) {
    if (d == 0) exit(EXIT_FAILURE);  // Обработка ошибки деления на ноль

    long long g = gcd(n, d);
    n /= g;
    d /= g;

    if (d < 0) {  // Если знаменатель отрицательный
        n = -n;
        d = -d;
    }

    return (rational_t){n, d};
}

long long rat_num(rational_t r) {
    return r.num;
}

unsigned long long rat_denom(rational_t r) {
    return r.denom;
}
