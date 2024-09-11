CC = gcc
CFLAGS = -Wall -Wextra -std=c11

all: primes

primes: primes.o
	$(CC) $(CFLAGS) -o primes primes.o

primes.o: primes.c
	$(CC) $(CFLAGS) -c primes.c

clean:
	rm -f *.o primes
