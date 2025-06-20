import ctypes

clib_file = ctypes.CDLL('./clib/libtest.so')

clib_file.calculate_primes.restype = ctypes.POINTER(ctypes.c_int)
clib_file.calculate_primes.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

clist = ctypes.c_int * 10000
numbers_to_check = clist()
numbers_count = 10000

clib_file.calculate_primes(numbers_to_check, numbers_count)

first_number = -1
second_number = 0

while True:
    first_number = int(input("Введите первое число: "))
    if(first_number == 0):
        break
    second_number = int(input("Введите второе число: "))
    second_number += 2
    while(first_number < second_number):
        count = 0
        minX = -1
        minY = -1
        number = 2
        while number <= first_number / 2:
            if numbers_to_check[number] == 1 and numbers_to_check[first_number - number] == 1:
                count += 1
                if(minX == -1):
                    minX = number
                    minY = first_number - number
            number += 1
        print(first_number, count, minX, minY)
        first_number += 2



