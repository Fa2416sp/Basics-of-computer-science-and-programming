#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include "search_funs.h"

int main(int argc, char *argv[])
{
	/* Проверка наличия аргументов */
	if (argc != 2) {
		fprintf(stderr,
				"Неверное количество аргументов\n");
		fprintf(stderr,
				"Использование: multiple_find \"dict_name.dict\"\n");
		exit(EXIT_FAILURE);
	}

	/* Файл словаря */
	FILE *dict = NULL;

	/* Шаблон для поиска */
	char pattern[LINE_BUFFER_SIZE] = "";

	int search_mode;

	/* Открываем файл словаря */
	dict = fopen(argv[1], "r");

	/* Проверяем существует ли файл словаря и возможно ли его прочитать */
	if (dict == NULL) {
		perror(argv[1]);
		exit(EXIT_FAILURE);
	}

	/* Буффер для хранения файла словаря */
	char *dictionary;
	/* Буффер для хранения найденых статей */
	char *out_buffer;

	dictionary = (char *) malloc(sizeof(char) * BUFFER_SIZE);
	out_buffer = (char *) malloc(sizeof(char) * BUFFER_SIZE);

	char *buffer_ptr = load_dictionary(dictionary, dict);

	/* Проверяем удалось ли записать весь файл в буффер */
	if (buffer_ptr == NULL) {
		fprintf(stderr,
				"Не удалось прочитать словарь\n");
		exit(EXIT_FAILURE);
	}

	/* Читаем строки до Ctrl+D */
	while (pattern[0] != EOF) {
		printf("Искать: ");
		int res = scanf("%s", &pattern[0]);
		/* Если Ctrl+D завершаем выполнение */
		if (res == EOF) {
			printf("\nЗавершение\n");
			return 0;
		}
		int found_something =
			filter_dictionary(pattern, dictionary, out_buffer);
		if (!found_something) {
			printf("Ничего не найдено!\n");
		} else {
			printf("%s\n", out_buffer);
			out_buffer[0] = '\0';
		}
	}
	/* Завершаем работу с файлом словаря */
	fclose(dict);
	/* И очищаем буфферы */
	free(dictionary);
	free(out_buffer);
	return 0;
}
