#    Демонстрация директив определения данных.
#    Переполнения для знакового и беззнакового сложения

#    Ассемблирование и редактирование связей - команда make

    .include "my-macro" # подключение файла с макроопределениями

.data # секция данных, распределение памяти

#                       Система счисления операнда

Diff_bases: .byte  65   # 10
    .byte  0101  # 8
    .byte  041   # 8
    .byte  0x41  # 16
    .byte  0X41  # 16

#    8      16     10
    .long  02345, 0x4E5, 1253

#    Выражения в директивах

Arifm_Expression:

    .byte 35+30, 20+45
    .byte 70-5, 80-15

Str:    .ascii  "abc ABC 123"
Str1:   .ascii  "Две капли сверкнут, сверкнут"
Str2:   .asciz  "на дне!"

B1:        .byte   255
B2:        .byte   240
Bm1:       .byte   -1
Bp1:       .byte   +1
B_zn_min:  .byte   -128
B_zn_max:  .byte   +127
BBB:       .byte   15,16,31,32,63,64
S1:        .short  255
S2:        .short  240
W_bzn_max: .short  65535
W_zn_min:  .short  -32768
W_zn_max:  .short  +32767
SSS:       .short  15,16,31,32,63,64
L1:        .long   4294967295
Il:        .int    4294967295
I1:        .int    -2147483648
I2:        .int    +2147483647
Q:         .quad   -2147483648

.text # секция команд

.global _start # точка входа

_start:
    movw    S1, %ax    # слово 255
    addw    S2, %ax    # + слово 240 = 495
            # НЕТ переполнения

    sub     %eax,%eax
    movb    B1, %al    # байт 255
    addb    B2, %al    # + 240
    jc      UnsignedOverflowb
    nop
    nop

UnsignedOverflowb:
    sub     %eax,%eax
    movw    W_bzn_max,%ax    # max беззнаковое слово
    addw    $1,%ax        # +1 к нему
    jc      UnsignedOverflow_w
    nop
    nop

UnsignedOverflow_w:
    sub     %eax,%eax
    movw    W_zn_max, %ax    # max знаковое слово
    addw    $1, %ax        # +1 к нему
    jo      SignedOverflow
    nop
    nop

SignedOverflow:
    sub     %eax, %eax
    movw    W_zn_min, %ax    # min знаковое слово
    subw    $1, %ax        # -1 от него
    jo      SignOver
    nop
    nop

SignOver:

    Finish # конец работы, возврат в ОС (макро из файла my-macro)
    .end   # последняя строка исходного текста
