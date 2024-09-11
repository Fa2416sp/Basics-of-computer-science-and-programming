# 1 Работа по Основам информатики и программирования 
## Hello-Students

### **1 Запуск Linux** 
- Тут без комментариев. Люди мы все взрослые так что справился    
### **2 Создание каталогов:**
- Откройте терминал. `ctrl+alt+t`
- Создайте каталог inf в домашнем каталоге:
```shell
mkdir ~/inf
```
- Внутри каталога inf создайте каталог task1:
```shell
mkdir ~/inf/task1
```

### **3 Создание файла main.c:**
- Откройте `vim` и создайте файл `main.c` в каталоге `task1`:
```shell
vim ~/inf/task1/main.c
```
- Вставьте следующий код, заменив `First Last` на ваше имя и фамилию, а `student@cs.petrsu.ru` на ваш адрес электронной почты
```main.c
/**
 * main.c -- программа "Hello, students!"
 *
 * Copyright (c) 2022, alex <alex-tabota@yandex.ru>
 *
 * This code is licensed under MIT license.
 */

#include <stdio.h>

int main()
{
    /* Выводим приветствие */
    fprintf(stdout, "Hello, students!\n");

    return 0;
}
```
### **4 Создание Makefile**
- В том же каталоге `task1` создайте файл `Makefile`:
```Shell
vim ~/inf/task1/Makefile
```
- Вставьте следующий код:
```Makefile
# цель по умолчанию (при вызове make или make task1)
# собираем программу task1 из объектного файла task1.o
task1: main.o
        gcc -g -O0 -o task1 main.o

main.o: main.c
        gcc -g -O0 -c main.c

# цель clean (при вызове make clean)
# удаляем программу и объектные файлы
clean:
        rm task1 *.o

# цель indent для форматирования кода
indent:
        indent -kr -nut main.c

```

### **5 Сборка программы :**
- В терминале перейдите в каталог `task1` и выполните команду `make`:
```shell
cd ~/inf/task1
make
```

### **6 Проверка работы программы :**
- Запустите программу:
```Shell
./task1
```
- Результат выполнения программы:
```Shell
Hello, students!
```
### **7 Форматирование кода :**
- Выполните команду `make indent` для форматирования кода:
```Shell
make indent
```
