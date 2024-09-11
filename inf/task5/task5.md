## 1. Создай каталог `task5` в каталоге `inf` и перейдём в него.
```Shell
mkdir ~/inf/task5
cd ~/inf/task5
```

## 2. В каталоге `inf/task5` создай файлы `rational.h`.
### rational.h:
```C
#ifndef RATIONAL_H
#define RATIONAL_H

typedef struct {
    int num;
    unsigned int denom;
} rational_t;

/*
 * Возвращает рациональное число, получаемое как результат деления
 * n на d.
 */
rational_t rational(long n, long d);

/*
 * Возвращает числитель рационального числа r.
 */
long rat_num(rational_t r);

/*
 * Возвращает знаменатель рационального числа r.
 */
long rat_denom(rational_t r);

#endif
```

## 3. Реализация функций в `rational.c`
### rational.c:
```C
#include "rational.h"
#include <stdlib.h>

static long gcd(long a, long b) {
    while (b != 0) {
        long t = b;
        b = a % b;
        a = t;
    }
    return a;
}

rational_t rational(long n, long d) {
    if (d == 0) {
        // Обработка ошибки деления на ноль
        exit(EXIT_FAILURE);
    }
    long g = gcd(abs(n), d);
    rational_t result = { n / g, d / g };
    if (result.denom < 0) {
        result.num = -result.num;
        result.denom = -result.denom;
    }
    return result;
}

long rat_num(rational_t r) {
    return r.num;
}

long rat_denom(rational_t r) {
    return r.denom;
}
```
## 4. Модуль для выполнения арифметических операций `rat_math.c`
### rat_math.c:
```C
#include "rational.h"

rational_t rat_add(rational_t a, rational_t b) {
    return rational(rat_num(a) * rat_denom(b) + rat_num(b) * rat_denom(a),
                    rat_denom(a) * rat_denom(b));
}

rational_t rat_sub(rational_t a, rational_t b) {
    return rational(rat_num(a) * rat_denom(b) - rat_num(b) * rat_denom(a),
                    rat_denom(a) * rat_denom(b));
}

rational_t rat_mul(rational_t a, rational_t b) {
    return rational(rat_num(a) * rat_num(b), rat_denom(a) * rat_denom(b));
}

rational_t rat_div(rational_t a, rational_t b) {
    return rational(rat_num(a) * rat_denom(b), rat_denom(a) * rat_num(b));
}
```
## 5. Модуль для ввода/вывода `rat_io.c`
### rat_io.c:
```C
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
```
## 6. Программа калькулятора `calc.c`
### calc.c
```C
#include "rational.h"
#include "rat_math.c"
#include "rat_io.c"
#include <stdio.h>
#include <string.h>

int main() {
    char input[100];
    rational_t last_result = {0, 1};

    while (fgets(input, sizeof(input), stdin)) {
        char op;
        char num1[50], num2[50];
        sscanf(input, "%s %c %s", num1, &op, num2);

        rational_t a = strcmp(num1, "last") == 0 ? last_result : rat_parse(num1);
        rational_t b = strcmp(num2, "last") == 0 ? last_result : rat_parse(num2);
        rational_t result;

        switch (op) {
            case '+': result = rat_add(a, b); break;
            case '-': result = rat_sub(a, b); break;
            case '*': result = rat_mul(a, b); break;
            case '/': result = rat_div(a, b); break;
            default: continue;
        }

        last_result = result;
        printf("= ");
        rat_print(result);
    }

    return 0;
}
```
## 7. Makefile для сборки
### Makefile:
```Macefile
# Makefile для сборки библиотеки и программы calc

all: calc

rational.o: rational.c rational.h
    gcc -c -fPIC rational.c -o rational.o

rat_math.o: rat_math.c rational.h
    gcc -c -fPIC rat_math.c -o rat_math.o

rat_io.o: rat_io.c rational.h
    gcc -c -fPIC rat_io.c -o rat_io.o

librational.a: rational.o rat_math.o rat_io.o
    ar -rcs librational.a rational.o rat_math.o rat_io.o

calc.o: calc.c rational.h
    gcc -c calc.c -o calc.o

calc: librational.a calc.o
    gcc -o calc calc.o -L. -lrational

clean:
    rm -f *.o *.a calc
```

## 8. Проверим программу 
### Собираем программу 
```Shell
make
```

### Запуск программы:
```Shell
./calc
```

### Введём  выражение
```Shell 
1/2 + 1/3
```

### Вывод программы 
```Shell
= 5/6
```