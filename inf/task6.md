## пример кода на С:
```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAXLINE 1023

void show_entries(const char *pattern, FILE *stream);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Неправильное число аргументов.\nИспользование: %s файл_словаря\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *dict = fopen(argv[1], "r");
    if (!dict) {
        perror("Ошибка открытия файла");
        return EXIT_FAILURE;
    }

    char pattern[MAXLINE + 1];
    printf("Введите шаблон для поиска: ");
    if (scanf("%1023s", pattern) != 1) {
        fprintf(stderr, "Ошибка ввода шаблона\n");
        fclose(dict);
        return EXIT_FAILURE;
    }

    show_entries(pattern, dict);

    fclose(dict);
    return EXIT_SUCCESS;
}

void show_entries(const char *pattern, FILE *stream) {
    char current_line[MAXLINE + 1];
    int matched_entry = 0;

    while (fgets(current_line, MAXLINE, stream) != NULL) {
        if (!isspace(current_line[0])) {
            matched_entry = (strstr(current_line, pattern) != NULL);
        }
        if (matched_entry) {
            printf("%s", current_line);
        }
    }
}
```

## Makefile: 
```Makefile
# Makefile для сборки программы dict1

# Компилятор
CC = gcc

# Флаги компилятора
CFLAGS = -Wall -Wextra -std=c99

# Имя исполняемого файла
TARGET = dict1

# Исходные файлы
SRCS = dict1.c

# Правило по умолчанию
all: $(TARGET)

# Правило сборки исполняемого файла
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

# Правило очистки
clean:
	rm -f $(TARGET)
```
## выполнение программы 
### Запуск программы: 
```Shell
./dict1 mueller.dict
```
### Вывод:
```Shell
Введите шаблон для поиска:
```
Введём `cause`
### Вывод программы:
```Shell
'cause

  [kɔz] _уст. = because
because

  [bɪˈkɔz] _cj.

    1) потому что; так как

    2): because of (употр. как предлог) из-за, вследствие
cause

  [kɔ:z]

    1. _n.

      1) причина

      2) основание; мотив, повод (for)

      3) дело; to support the cause of the workers защищать дело рабочего
      класса; the cause of peace дело мира; to make common cause with smb.
      объединяться с кем-л. ради общего дела; in the cause of science ради
      (или во имя) науки; in a good cause чтобы сделать добро

      4) _юр. дело, процесс; to plead a cause защищать дело в суде

      5) _attr.: cause celebre знаменитый судебный процесс

    2. _v.

      1) быть причиной, причинять, вызывать; to cause smb. to be informed
      поставить кого-л. в известность

      2) заставлять; to cause a thing to be done велеть что-л. выполнить
causeless

  [ˈkɔ:zlɪs] _a. беспричинный; необоснованный
causelist

  [ˈkɔ:zlɪst] _n. _юр. список дел к слушанию
causer

  [ˈkɔ:zə] _n. виновник
causeway

  [ˈkɔ:zweɪ]

    1. _n.

      1) мостовая; мощёная дорожка; тротуар

      2) дамба; гать

    2. _v.

      1) строить плотину, дамбу

      2) мостить
causey

  [ˈkɔ:zɪ] = causeway
uncaused

  [ˈʌnˈkɔ:zd] _a.

    1) беспричинный

    2) извечный
```
