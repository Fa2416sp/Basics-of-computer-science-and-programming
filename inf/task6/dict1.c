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
