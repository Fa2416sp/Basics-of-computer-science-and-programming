#include <stdlib.h>
#include <stdbool.h>
#include "test.h"

int* calculate_primes(int limit, int* count) {
    bool* is_prime = malloc((limit + 1) * sizeof(bool));
    for (int i = 0; i <= limit; i++) is_prime[i] = true;

    is_prime[0] = is_prime[1] = false;

    for (int i = 2; i * i <= limit; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                is_prime[j] = false;
            }
        }
    }

    // Подсчёт количества простых
    *count = 0;
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) (*count)++;
    }

    // Заполнение массива простыми
    int* primes = malloc((*count) * sizeof(int));
    int index = 0;
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) primes[index++] = i;
    }

    free(is_prime);
    return primes;
}
