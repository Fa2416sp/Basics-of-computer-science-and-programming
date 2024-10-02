spacexplore: spacexplore.o
	gcc -o spacexplore spacexplore.o `pkg-config --libs sdl`

spacexplore.o: spacexplore.c
	gcc -c -Wall -Wextra -Wno-switch spacexplore.c `pkg-config --cflags sdl`

clean:
	rm spacexplore *.o
