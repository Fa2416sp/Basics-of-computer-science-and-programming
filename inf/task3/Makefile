CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g

all: lychrel

lychrel: lychrel.o
	$(CC) $(CFLAGS) -o lychrel lychrel.o

lychrel.o: lychrel.c
	$(CC) $(CFLAGS) -c lychrel.c

clean:
	rm -f lychrel lychrel.o

indent:
	indent -kr -nut lychrel.c

