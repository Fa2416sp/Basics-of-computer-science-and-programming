.text # секция команд процесора

.type  Sum, @function                   # функция циклической обработки массива
.globl Sum

Sum:

    pushl %ebp                          # сохранить в стеке значение, бывшее в вызывающей
    movl  %esp, %ebp                    # обеспечить адресный доступ к параметрам и
                                        # локальным переменнным в стеке путем базовой
                                        # адресации через ebp
    subl  $4, %esp                      # завести 4-х байтовую локальную переменную 

    movl 12(%ebp),%edx
    subl %eax, %eax
    subl %ecx, %ecx                     # инициализация счетчика цикла

Next:
    movl (%edx,%ecx,4), %ebx            # Выносим из массива цифру

    addl %ebx, %eax                     # Складываем

    incl %ecx                           # Итератор
    cmpl 8(%ebp), %ecx
    jne Next

    movl %ebp, %esp
    popl %ebp
    ret

.end
