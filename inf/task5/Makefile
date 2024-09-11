# Makefile для сборки библиотеки и программы calc

all: calc

rational.o: rational.c rational.h
	gcc -c -fPIC rational.c -o rational.o

rat_math.o: rat_math.c rational.h
	gcc -c -fPIC rat_math.c -o rat_math.o

rat_io.o: rat_io.c rational.h
	gcc -c -fPIC rat_io.c -o rat_io.o

librational.a: rational.o rat_math.o rat_io.o
	ar -rcs librational.a rational.o rat_math.o rat_io.o

calc.o: calc.c rational.h
	gcc -c calc.c -o calc.o

calc: librational.a calc.o
	gcc -o calc calc.o -L. -lrational

clean:
	rm -f *.o *.a calc
