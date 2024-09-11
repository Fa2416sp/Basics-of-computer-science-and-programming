## 1. Создай каталог `task4` в каталоге `inf` и перейдём в него.
```Shell
mkdir ~/inf/task4
cd ~/inf/task4
```
## 2. В каталоге `inf/task4` создай файлы `primes.c` и `Makefile`.
### primes.c:
```C
#include <stdio.h>
#include <stdlib.h>

void calculate_primes(int primes[], int n) {
    for (int i = 0; i <= n; i++) {
        primes[i] = 1; // Изначально считаем все числа простыми
    }
    primes[0] = primes[1] = 0; // 0 и 1 не являются простыми числами

    for (int i = 2; i * i <= n; i++) {
        if (primes[i]) {
            for (int j = i * i; j <= n; j += i) {
                primes[j] = 0; // Числа, кратные i, не являются простыми
            }
        }
    }
}

int main() {
    int n;
    printf("Введите значение n: ");
    scanf("%d", &n);

    int *primes = (int *)malloc((n + 1) * sizeof(int));
    if (primes == NULL) {
        printf("Ошибка выделения памяти\n");
        return 1;
    }

    calculate_primes(primes, n);

    printf("Простые числа до %d:\n", n);
    for (int i = 2; i <= n; i++) {
        if (primes[i]) {
            printf("%d ", i);
        }
    }
    printf("\n");

    free(primes);
    return 0;
}
```
### Makefile
```Makefile
CC = gcc
CFLAGS = -Wall -Wextra -std=c11

all: primes

primes: primes.o
	$(CC) $(CFLAGS) -o primes primes.o

primes.o: primes.c
	$(CC) $(CFLAGS) -c primes.c

clean:
	rm -f *.o primes
```

### Теперь ты можешь скомпилировать и запустить программу для нахождения простых чисел. Для этого выполни команды:
```Shell
make
```
## 3. Проверим программу 
### Запуск программы:
```Shell
./primes
```
### Вывод программы:
```Shell
Введите значение n: 21
Простые числа до 21:
2 3 5 7 11 13 17 19 
```
