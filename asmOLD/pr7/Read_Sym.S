.globl Numbers

.text

.type Read_Sym, @function
.globl Read_Sym

Read_Sym:

    pushl %ebp                  # %ebp вызывающей -> стек
    movl %esp, %ebp             # обеспечить адресный доступ к параметрам и
                                # локальным переменным в стеке путем базовой
                                # адресации через ebp

    subl $4, %esp               # завести локальную перемен. в Кадре 1
    movl $0,-4(%ebp)

    subl %ecx, %ecx             # иницируем цикла по байтам Symbols

NextSym:

    movl 12(%ebp), %edx         # адрес P2 - массива в %edx

    subl %ebx, %ebx             # Отчищаем %ebx

    movb (%edx,%ecx,1), %bl     # Заносим в %ebx символ из строки

    pusha

    cmpb $'9', %bl
    ja Ret_error
    cmpb $'0', %bl
    jb Ret_error

    pushl %ebx

    call Trans_Sym

    addl $4,%esp                # очистить стек от параметров
    jmp Check

Ret_error:

    movl $0,%eax                # для возврата если код не символ цифры
    incl -4(%ebp)

Check:
    movl %eax, Numbers(,%ecx,4) # Заносим число в массив

    popa                        # восстановть регистры 

    incl %ecx                   # наращиваем счетчик цикла
    cmpl 8(%ebp), %ecx          # счетчик цикла равен первому параметру?
    jne NextSym

    movl %ebp, %esp             # восстановить указатель стека
    popl %ebp                   # восстановить ebp

    ret                         # возврат в вызывающую



.type Trans_Sym, @function
.globl Trans_Sym

Trans_Sym:

    pushl %ebp                  # сохранить в стеке значение, бывшее в вызывающей
    movl %esp, %ebp             # обеспечить адресный доступ к параметрам и.
                                # локальным переменнным в стеке путем базовой.
                                # адресации через ebp

    movl 8(%ebp), %eax          # параметр в eax

    subl $0x30, %eax            # получение числового значения

    movl %ebp, %esp             #восстановить указатель стека
    popl %ebp                   # восстановить ebp

    ret

.end
