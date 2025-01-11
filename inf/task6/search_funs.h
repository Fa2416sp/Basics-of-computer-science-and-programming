/* Максимальный размер строки (для dict1.c) */
#ifndef MAXLINE
	#define MAXLINE 1023
#endif

/* Размер буффера словаря в байтах (dict2.c) */
#ifndef BUFFER_SIZE
	#define BUFFER_SIZE 1024 * 1024 * 10
#endif

/* Размер буффера строки (dict2.c) */
#ifndef LINE_BUFFER_SIZE
	#define LINE_BUFFER_SIZE 1024
#endif

#ifndef CONTAINS
	#define CONTAINS 0
#endif

#ifndef AT_BEGIN
	#define AT_BEGIN 1
#endif

#ifndef AT_END
	#define AT_END 2
#endif

#ifndef EQUALLY
	#define EQUALLY 3
#endif

#ifndef FALSE
	#define FALSE 0
#endif

#ifndef TRUE
	#define TRUE 1
#endif

char get_last_char(char *str);
void remove_non_word(char *str, int mode);
void array_to_lower(char *arr);
int get_search_mode(char* template);
int compare_end(char *str, char *end);
int compare_begin(char *str, char *begin);
int show_entries(char *template, FILE *dict, int search_mode);
int filter_dictionary(char *template, char *dict, char* out_buffer);
char* load_dictionary(char *dictionary, FILE *stream);
