.include "my-macro"

.bss
    .lcomm string, 16           # сюда будем класть символы для вывода

.data
    .lcomm c, 1                 # буфер для символа
    result: .long 0             # здесь будет хранится сумма цифр

    k: .long 0
    l: .long 0
    i: .long 0
    str: .long 24
    stb: .long 4
    res: .long 0
    ansver: .long 0, 0, 0, 0, 0, 0

    matrix:
        .long  4000000000,   2,   3,   4,   5,   6
        .long  7,   8,   9,  10,  11,  12
        .long 13,  14,  15,  16,  17,  18
        .long 19,  20,  21,  22,  23,  24
        .long 25,  26,  27,  28,  29,  30
        .long 31,  32,  33,  34,  35,  36

.text
    .global _start

_start:
    nop

show_prompt_k:
    subl %edx, %edx

    # Как-то отчистить c
    Puts "Input k" # ввод пользователя

k_input:
    Getchar $c                  # макровызов ввода байта из stdin в промежуточный буфер c
    cmpl $0, %eax               # EOF?
    je stop

    cmpb $'\n', c               # код символа равен новой строке ?
    je k_input
    cmpb $'6', c                # код больше кода символа '6' ?
    ja print_err_msg_k          # ДА - на вывод сообщения об ошибке
    cmpb $'1', c                # код меньше кода символа '0' ?
    jb print_err_msg_k          # ДА - на вывод сообщения об ошибке

    movb c, %bl                 # переводим символ цифры в цифру

    subb $48, %bl

    movb %bl, k

show_prompt_l:
    # Как-то отчистить c
    Puts "Input l" # ввод пользователя

l_input:
    Getchar $c                  # макровызов ввода байта из stdin в промежуточный буфер c
    cmpl $0, %eax               # EOF?
    je stop

    cmpb $'\n', c               # код символа равен новой строке ?
    je l_input
    cmpb $'6', c                # код больше кода символа '6' ?
    ja print_err_msg_l          # ДА - на вывод сообщения об ошибке
    cmpb $'1', c                # код меньше кода символа '0' ?
    jb print_err_msg_l          # ДА - на вывод сообщения об ошибке

    movb c, %bl                 # переводим символ цифры в цифру

    subb $48, %bl

    movb %bl, l

matrixres:
    subl %ecx, %ecx                     # отчистка ecx
    subl %ebx, %ebx                     # отчистка ebx
    movl $0, %ecx                       # итератор

    nextdigit:
        movl $0, res

        subl %esi, %esi                 # отчистка esi

        movl k, %ebx                    # занесение первого ввода в ebx
        decl %ebx                       # так как читаем массив с 0, то уменьшаем ebx на один
        imull str, %ebx                 # умножаем ebx на 24, т.к. каждая строка начинается с i*24
        movl matrix(%ebx, %ecx, 4), %esi# добавляем к значению esi элемент матрицы
        addl %esi, res
        jc SignedOverflow

        movl l, %ebx                    # занесение второго ввода в ebx
        decl %ebx                       # так как читаем массив с 0, то уменьшаем ebx на один
        movl %ecx, i                    # костыль но все же запоминаем в i итератор, чтобы потом заносить esi по нему
        imull str, %ecx                 # умножаем ecx на 24, т.к. каждая строка начинается с i*24
        movl matrix(%ecx, %ebx, 4), %esi# добавляем к значению esi элемент матрицы
        addl %esi, res
        jc SignedOverflow

        Output res

        movl i, %ecx
        incl %ecx                       # увеличиваем индекс
        cmp $6, %ecx                    # проверяем нужно ли дальше
        jne nextdigit

    Puts "\n"
    Puts "\n"
    Puts "\n"


jmp show_prompt_k

print_err_msg_k:
    Puts "Wrong k"
    jmp show_prompt_k

print_err_msg_l:
    Puts "Wrong l"
    jmp show_prompt_l

SignedOverflow:
    Puts "Oversum!!!"
    Exit $0

stop:
    Exit $0
.end



