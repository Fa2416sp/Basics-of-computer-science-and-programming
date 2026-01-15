.include "my-macro"

.bss
    .lcomm string, 16           # Сюда будем класть символы для вывода

.data
    .lcomm c, 1                 # Буфер для символа
    .lcomm kostyl, 2            # Костыль
    .lcomm last_is_digit, 1     # Флаг валидной цифры перед Enter
    result: .short 0            # Здесь будет хранится сумма цифр
    ten: .long 10               # Переменные для деления в my-macro
    eig: .long 8
    two: .long 2

.text
    .global _start
_start:
    nop

show_prompt:
    Puts "Введите цифры!!!!!!!!"

input_char:
    Getchar $c                  # Макровызов ввода байта из stdin в промежуточный буфер c

    cmpl $0, %eax               # Наступило событие EOF (конец файла stdin) ?
    je stop                     # Да - на завершение программы

    cmpb $'\n', c               # Код символа равен новой строке ?
    je enter
    cmpb $'9', c                # Код больше кода символа '9' ?
    ja print_err_msg            # Да - на вывод сообщения об ошибке
    cmpb $'0', c                # Код меньше кода символа '0' ?
    jb print_err_msg            # Да - на вывод сообщения об ошибке

    movb c, %bl                 # Переводим символ цифры в цифру
    subb $48, %bl

    movb %bl, kostyl            # Сохраняем последний символ перед enter
    movb $1, last_is_digit

    jmp input_char

enter:
    cmpb $0, last_is_digit
    je reset_enter
    sub %bx, %bx                # Очищаем bx от enter
    movb kostyl, %bl            # Заносим последний символ перед enter
    addw %bx, result            # увеличиваем result
    jc SignedOverflow           # проверяем знаковое переполнение

reset_enter:
    movb $0, last_is_digit
    jmp show_prompt

print_err_msg:
    movb $0, last_is_digit
    Puts "Не цифровая клавиша. Повторите ввод"
    jmp input_char             # Идем на ввод следующего символа

SignedOverflow:
    Puts "Переполнение суммы!!!"
    Exit $0

stop:
    Puts "Сумма:"
    PutsSumm
    Exit $0
.end
