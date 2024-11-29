#include "rat_math.h"
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>  // Добавляем этот заголовок для использования типа bool

static bool will_addition_overflow(long long a, long long b) {
    return (b > 0 && a > LLONG_MAX - b) || (b < 0 && a < LLONG_MIN - b);
}

static bool will_multiplication_overflow(long long a, long long b) {
    if (a == 0 || b == 0) return false;
    return (a > 0) ? (b > 0 && a > LLONG_MAX / b) || (b < 0 && b < LLONG_MIN / a)
                   : (b > 0 && a < LLONG_MIN / b) || (b < 0 && b < LLONG_MAX / a);
}

static long long gcd(long long a, long long b) {
    while (b != 0) {
        long long t = b;
        b = a % b;
        a = t;
    }
    return a;
}

rational_t rat_add(rational_t a, rational_t b) {
    long long common_denom = gcd(a.denom, b.denom);
    long long a_num = a.num * (b.denom / common_denom);
    long long b_num = b.num * (a.denom / common_denom);
    long long num = a_num + b_num;
    unsigned long long denom = a.denom * (b.denom / common_denom);

    if (will_addition_overflow(a_num, b_num) || will_multiplication_overflow(a.denom, (b.denom / common_denom))) {
        exit(EXIT_FAILURE);  // Обработка переполнения
    }

    return rational(num, denom);
}

rational_t rat_sub(rational_t a, rational_t b) {
    long long common_denom = gcd(a.denom, b.denom);
    long long a_num = a.num * (b.denom / common_denom);
    long long b_num = b.num * (a.denom / common_denom);
    long long num = a_num - b_num;
    unsigned long long denom = a.denom * (b.denom / common_denom);

    if (will_addition_overflow(a_num, -b_num) || will_multiplication_overflow(a.denom, (b.denom / common_denom))) {
        exit(EXIT_FAILURE);  // Обработка переполнения
    }

    return rational(num, denom);
}

rational_t rat_mul(rational_t a, rational_t b) {
    if (will_multiplication_overflow(a.num, b.num) || will_multiplication_overflow(a.denom, b.denom)) {
        exit(EXIT_FAILURE);  // Обработка переполнения
    }
    long long num = a.num * b.num;
    unsigned long long denom = a.denom * b.denom;
    return rational(num, denom);
}

rational_t rat_div(rational_t a, rational_t b) {
    if (b.num == 0 || will_multiplication_overflow(a.num, b.denom) || will_multiplication_overflow(a.denom, b.num)) {
        exit(EXIT_FAILURE);  // Обработка деления на ноль или переполнения
    }
    long long num = a.num * b.denom;
    unsigned long long denom = a.denom * b.num;
    return rational(num, denom);
}
