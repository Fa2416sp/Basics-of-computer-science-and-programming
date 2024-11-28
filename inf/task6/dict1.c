#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAXLINE 1023

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Неправильное число аргументов.\nИспользование: %s файл_словаря\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE* dict = fopen(argv[1], "r");
    if (!dict) {
        perror("Ошибка открытия файла словаря");
        return EXIT_FAILURE;
    }

    char current_line[MAXLINE + 1] = "";    
    int requested_entry_number;
    int current_entry_number = 0;

    if (scanf("%d", &requested_entry_number) != 1) {
        fprintf(stderr, "Ошибка ввода номера статьи.\n");
        fclose(dict);
        return EXIT_FAILURE;
    }

    int matched_entry = 0;

    while (fgets(current_line, MAXLINE, dict) != NULL) {
        if (!isspace(current_line[0])) {
            current_entry_number++;
            matched_entry = (current_entry_number == requested_entry_number);
        }

        if (matched_entry) {
            printf("%s", current_line);
        }
    }

    fclose(dict);
    return EXIT_SUCCESS;
}
