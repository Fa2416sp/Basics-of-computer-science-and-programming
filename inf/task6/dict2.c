#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAXSIZE 10485760 // 10 MB

char* load_dictionary(char *dictionary, FILE *stream)
{
    size_t total_read = fread(dictionary, 1, MAXSIZE, stream);
    if (total_read >= MAXSIZE) {
        fprintf(stderr, "Слишком большой файл словаря.\n");
        return NULL;
    }
    dictionary[total_read] = '\0';
    return dictionary;
}

void filter_dictionary(const char *pattern, const char *dictionary)
{
    const char *dict_ptr = dictionary;
    size_t pattern_len = strlen(pattern);
    int match_start = pattern[0] == '^';
    int match_end = pattern[pattern_len - 1] == '$';
    
    if (match_start) pattern++;
    if (match_end) pattern_len--;

    while (*dict_ptr != '\0') {
        const char *entry_start = dict_ptr;
        while (*dict_ptr != '\0' && *dict_ptr != '\n') {
            dict_ptr++;
        }

        size_t entry_len = dict_ptr - entry_start;
        int match = (match_start && strncmp(entry_start, pattern, pattern_len) == 0) ||
                    (match_end && strncmp(dict_ptr - pattern_len, pattern, pattern_len) == 0) ||
                    (!match_start && !match_end && strstr(entry_start, pattern) != NULL);

        if (match) {
            fwrite(entry_start, 1, entry_len, stdout);
            printf("\n");
        }

        if (*dict_ptr == '\n') dict_ptr++;
    }
}

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

    char *dictionary = malloc(MAXSIZE + 1);
    if (!dictionary) {
        fprintf(stderr, "Ошибка выделения памяти.\n");
        fclose(dict);
        return EXIT_FAILURE;
    }

    if (!load_dictionary(dictionary, dict)) {
        free(dictionary);
        fclose(dict);
        return EXIT_FAILURE;
    }

    fclose(dict);

    char pattern[100];
    while (fgets(pattern, sizeof(pattern), stdin)) {
        pattern[strcspn(pattern, "\n")] = '\0';  // Удаляем символ новой строки
        filter_dictionary(pattern, dictionary);
    }

    free(dictionary);
    return EXIT_SUCCESS;
}
