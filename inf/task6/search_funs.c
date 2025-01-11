#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include "search_funs.h"

/* Получение последнего символа с строке */
char get_last_char(char *str)
{
	int last_n = strlen(str) - 1;
	return str[last_n];
}

/* Удаление вспомогательных символов из шаблона поиска */
void remove_non_word(char *str, int mode)
{
	if (mode == 0) {
		return;
	} else if (mode == 1) {
		int last_n = strlen(str) - 1;
		for (int i = 0; i < last_n; i++)
			str[i] = str[i + 1];
		str[last_n] = '\n';
		str[last_n + 1] = '\0';
	} else if (mode == 2) {
		int last_n = strlen(str) - 1;
		str[last_n] = '\n';
		str[last_n + 1] = '\0';
	} else if (mode == 3) {
		int last_n = strlen(str) - 1;
		for (int i = 0; i < last_n; i++)
			str[i] = str[i + 1];
		str[last_n - 1] = '\n';
		str[last_n] = '\0';
	} else {
		return;
	}
}

/* Перевод строки в нижний регистр */
void array_to_lower(char *arr)
{
	int last_n = strlen(arr) - 1;
	for (int i = 0; i < last_n; i++) {
		arr[i] = tolower(arr[i]);
	}
}

/* Сравнение конца строки "str" со строкой "end" */
int compare_end(char *str, char *end)
{
	int str_n = strlen(str) - 1;
	int end_str_n = strlen(end) - 1;
	if (end_str_n > str_n) {
		return FALSE;
	}
	int sub_i = str_n - end_str_n;
	for (int i = 0; i < end_str_n; i++) {
		if (str[sub_i + i] != end[i]) {
			return FALSE;
		}
	}
	return TRUE;
}

/* Сравнение начала строки "str" со строкой "begin" */
int compare_begin(char *str, char *begin)
{
	int str_n = strlen(str) - 1;
	int begin_str_n = strlen(begin) - 1;
	if (begin_str_n > str_n) {
		return FALSE;
	}
	for (int i = 0; i < begin_str_n; i++) {
		if (str[i] != begin[i]) {
			return FALSE;
		}
	}
	return TRUE;
}

/* Определение режима поиска
 * Режимы поиска:
 * 0 - шаблон есть в слове ("шаблон")
 * 1 - шаблон в начале слова ("^шаблон")
 * 2 - шаблон в конце слова ("шаблон$")
 * 3 - точное совпадение слова и шаблона ("^шаблон$")
 */
int get_search_mode(char *pattern)
{
	int search_mode = EQUALLY;
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
	return search_mode;
}

/* Поиск и печать статей. Возвращает "0" если ничего не найдено */
/* Для dict1.c, без загрузки в буффер */
int show_entries(char *pattern, FILE * dict, int search_mode)
{
	/* Текущая строка */
	char current_line[MAXLINE + 1] = "";
	/* Копия текущей строки (для проверки без учета регистра) */
	char line_copy[MAXLINE + 1] = "";

	/* Флаг = 1, если найдена хотя бы одна статья */
	int found_something = 0;

	/* Флаг соответствия текущей статьи условию отбора */
	int matched_entry = 0;

	/* Просматриваем словарь, печатая строки запрошенной статьи */
	while (fgets(current_line, MAXLINE, dict) != NULL) {
		/* Копируем текущую строку в line_copy
		 * чтобы сравнить в нижнем регистре
		 * но напечать как в словаре
		 * (например название с большой буквы)
		 */
		strcpy(line_copy, current_line);
		/* Если первый символ строки не является пробельным разделителем,
		   найдено начало новой словарной статьи */
		if (!isspace(line_copy[0])) {
			/* Текущая строка в нижний регистр */
			array_to_lower(&line_copy[0]);
			matched_entry = 0;

			switch (search_mode) {
			case CONTAINS:
				/* шаблон есть в строке */
				if (strstr(line_copy, pattern) != NULL) {
					matched_entry = 1;
				}
				break;
			case AT_BEGIN:
				/* шаблон есть в начале строки */
				if (compare_begin(&line_copy[0], pattern)) {
					matched_entry = 1;
				}
				break;
			case AT_END:
				/* шаблон есть в конце строки */
				if (compare_end(&line_copy[0], pattern)) {
					matched_entry = 1;
				}
				break;
			case EQUALLY:
				/* полное совпадение строки и шаблона */
				if (strcmp(line_copy, pattern) == 0) {
					matched_entry = 1;
				}
				break;
			}
		}
		found_something = found_something || matched_entry;
		if (matched_entry) {
			printf("%s", current_line);
		}
	}

	if (found_something) {
		return 1;
	} else {
		return 0;
	}
}

/* Загрузка словаря в буффер
 * stream - файл словаря
 * dictionary - буффер для сохранения данных из stream
 */
char *load_dictionary(char *dictionary, FILE * stream)
{
	/* Количество прочитанных символов (размер char = 1 байт) */
	int bytes_number = 0;

	/* Чтение всего словаря в буффер
	 * В bytes_number запишется количество символов в словаре
	 */
	bytes_number = fread(dictionary, 1, BUFFER_SIZE, stream);

	if (!feof(stream)) {
		return NULL;
	}

	dictionary[bytes_number] = EOF;
	return dictionary;
}

/* Поиск и печать статей. Возвращает "0" если ничего не найдено
 * pattern - шаблон поиска
 * dict - буффер словаря
 * out_buffer - буффер для результатов
 */
int filter_dictionary(char *pattern, char *dict, char *out_buffer)
{
	int search_mode = get_search_mode(&pattern[0]);
	remove_non_word(&pattern[0], search_mode);
	array_to_lower(&pattern[0]);
	/* Номер символа в текущей строке
	 * сбрасывается в 0 с каждой новой строкой
	 */
	int char_pos_in_line = 0;
	int char_pos_in_buff = 0;

	/* Текущая строка */
	char current_line[LINE_BUFFER_SIZE] = "";

	/* Копия текущей строки (для проверки без учета регистра) */
	char line_copy[LINE_BUFFER_SIZE] = "";

	/* Флаг = 1, если найдена хотя бы одна статья */
	int found_something = 0;

	/* Флаг соответствия текущей статьи условию отбора */
	int matched_entry = 0;

	/* Чтение словаря из буфера */
	while (dict[char_pos_in_buff] != EOF) {
		if (dict[char_pos_in_buff] != '\n'
			&& char_pos_in_line < LINE_BUFFER_SIZE) {
			/* Если не перевод строки, то записываем
			 * элемент буффера с текущую строку
			 */
			current_line[char_pos_in_line] = dict[char_pos_in_buff];
			char_pos_in_line++;
		} else {
			/* Если новая строка, то устанавливаем конец строки
			 * и обрабатываем строку
			 */
			current_line[char_pos_in_line] = '\n';
			current_line[char_pos_in_line + 1] = '\0';
			char_pos_in_line = 0;

			strcpy(line_copy, current_line);
			/* Если первый символ строки не является пробельным разделителем,
			   найдено начало новой словарной статьи */
			if (!isspace(line_copy[0])) {
				/* Текущая строка в нижний регистр */
				array_to_lower(&line_copy[0]);
				matched_entry = 0;

				switch (search_mode) {
				case CONTAINS:
					/* шаблон есть в строке */
					if (strstr(line_copy, pattern) != NULL) {
						matched_entry = 1;
					}
					break;
				case AT_BEGIN:
					/* шаблон есть в начале строки */
					if (compare_begin(&line_copy[0], pattern)) {
						matched_entry = 1;
					}
					break;
				case AT_END:
					/* шаблон есть в конце строки */
					if (compare_end(&line_copy[0], pattern)) {
						matched_entry = 1;
					}
					break;
				case EQUALLY:
					/* полное совпадение строки и шаблона */
					if (strcmp(line_copy, pattern) == 0) {
						matched_entry = 1;
					}
					break;
				}
			}
			found_something = found_something || matched_entry;
			if (matched_entry) {
				strcat(out_buffer, current_line);
			}
		}
		char_pos_in_buff++;
	}

	if (found_something) {
		return 1;
	} else {
		return 0;
	}
}
