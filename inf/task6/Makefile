all: single_find multiple_find

single_find: search_funs.o dict1.o
	gcc -g dict1.o search_funs.o -o single_find

dict1.o: dict1.c search_funs.h
	gcc -g -c dict1.c

multiple_find: search_funs.o dict2.o
	gcc -g dict2.o search_funs.o -o multiple_find

dict2.o: dict2.c search_funs.h
	gcc -g -c dict2.c

search_funs.o: search_funs.c search_funs.h
	gcc -g -c search_funs.c

clean:
	rm *.o single_find multiple_find

indent:
	indent -kr -ts4 *.c
