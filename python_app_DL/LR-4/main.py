import ctypes

# Загрузка библиотеки
lib = ctypes.CDLL('./libtest.so')

# Определение сигнатуры функции
lib.calculate_primes.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
lib.calculate_primes.restype = ctypes.POINTER(ctypes.c_int)

def get_primes(limit):
    count = ctypes.c_int()
    ptr = lib.calculate_primes(limit, ctypes.byref(count))
    primes = [ptr[i] for i in range(count.value)]
    return primes

def check_goldbach(limit):
    primes = get_primes(limit)
    prime_set = set(primes)

    for even in range(4, limit + 1, 2):
        found = False
        for p in primes:
            if p > even:
                break
            if even - p in prime_set:
                print(f"{even} = {p} + {even - p}")
                found = True
                break
        if not found:
            print(f"Гипотеза Гольдбаха не выполнена для {even}")
            return
    print("Гипотеза Гольдбаха выполнена для всех чётных чисел до", limit)

if __name__ == "__main__":
    check_goldbach(100)
