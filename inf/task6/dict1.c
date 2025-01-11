#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "search_funs.h"

int main(int argc, char *argv[])
{
	/* Проверка наличия аргументов */
	if (argc < 2) {
		printf("Не указан путь к словарю!\n");
		return 0;
	}

	/* Файл словаря */
	FILE *dict = NULL;

	/* Шаблон для поиска */
	char pattern[MAXLINE + 1] = "";

	int search_mode = EQUALLY;

	/* Открываем файл словаря */
	dict = fopen(argv[1], "r");

	/* Проверяем существует ли файл словаря и возможно ли его прочитать */
	if (dict == NULL) {
		printf
			("Словарь \"%s\" не существует или не доступен\n",
			 argv[1]);
		return 0;
	}

	/* Получаем шаблон для поиска */
	printf("Искать: ");
	scanf("%s", &pattern[0]);

	/* Определение типа поиска */
	if (pattern[0] == '^') {
		if (get_last_char(pattern) == '$') {
			/* точное совпадение */
			search_mode = EQUALLY;
		} else {
			/* шаблон в начале слова */
			search_mode = AT_BEGIN;
		}
	} else if (get_last_char(pattern) == '$') {
		/* шаблон в конце слова */
		search_mode = AT_END;
	} else {
		/* шаблон входит в слово */
		search_mode = CONTAINS;
	}

	/* убраем из шаблона символы "^" и "$" */
	remove_non_word(&pattern[0], search_mode);
	/* переврдим шаблон в нижний регистр */
	array_to_lower(&pattern[0]);

	int found_something = show_entries(pattern, dict, search_mode);

	/* Завершаем работу с файлом словаря */
	fclose(dict);

	if (!found_something) {
		printf("Ничего не найдено!\n");
	}

	return 0;
}
