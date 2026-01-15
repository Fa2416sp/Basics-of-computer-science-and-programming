#include <stdio.h>
#include <string.h>

// Объявление функций
void Read_Sym(int, char*);
int Sum(int, int* );

//Массив, где будем хранить числа
int Numbers[12];

int main()
{
    // Длина зависит от массива
    int len = sizeof(Numbers) / sizeof(Numbers[0]);

    // Строка
    char Symbols[len+1];
    strcpy(Symbols, "91A53B467C72\0");

    // Результат
    int sum_res;

    // Выводим строку ну для красоты и понимания как бы
    printf ("%s\n",Symbols);

    // Вызов функций
    Read_Sym(len, Symbols);
    sum_res = Sum(len, Numbers);

    // Печатаем результат сложения
    printf ("%d\n",sum_res);

    return 0;
}