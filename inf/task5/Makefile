CC = gcc
CFLAGS = -Wall -fPIC

OBJS = calc.o rational.o rat_math.o rat_io.o

all: calc

calc: $(OBJS)
	$(CC) -o calc $(OBJS)

calc.o: calc.c
	$(CC) $(CFLAGS) -c calc.c

rational.o: rational.c
	$(CC) $(CFLAGS) -c rational.c

rat_math.o: rat_math.c
	$(CC) $(CFLAGS) -c rat_math.c

rat_io.o: rat_io.c
	$(CC) $(CFLAGS) -c rat_io.c

clean:
	rm -f $(OBJS) calc
