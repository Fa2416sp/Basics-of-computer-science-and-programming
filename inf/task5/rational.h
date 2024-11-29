#ifndef RATIONAL_H
#define RATIONAL_H

typedef struct {
    long long num;  // Используем long long для числителя
    unsigned long long denom;  // Используем unsigned long long для знаменателя
} rational_t;

/*
 * Возвращает рациональное число, получаемое как результат деления n на d.
 */
rational_t rational(long long n, unsigned long long d);

/*
 * Возвращает числитель рационального числа r.
 */
long long rat_num(rational_t r);

/*
 * Возвращает знаменатель рационального числа r.
 */
unsigned long long rat_denom(rational_t r);

#endif
