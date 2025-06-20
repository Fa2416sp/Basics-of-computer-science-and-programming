import ctypes
test = ctypes.CDLL('./libtest.so')

test.addone.restype = ctypes.c_int
test.addone.argtypes = [ctypes.c_int]

print('ret func_addone', test.addone(5))

list1 = [1, 2, 3, 4]
list2 = ctypes.POINTER(ctypes.c_int)()
list3 = ctypes.c_int * 4
trash = list3()

test.changemas.restype = ctypes.POINTER(ctypes.c_int)
test.changemas.argtypes = [ctypes.POINTER(ctypes.c_int)]
print('ret func_changemas', test.changemas(trash))
print(trash[0])
print(list1)
