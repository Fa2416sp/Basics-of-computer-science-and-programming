c-as: call-as.c Read_Sym.o Sum.o
	gcc -m32 -gstabs+ -o c-as call-as.c Read_Sym.o Sum.o

Sum.o: Sum.S
	as --32 -gstabs+ -o Sum.o Sum.S

Read_Sym.o: Read_Sym.S
	as --32 -gstabs+ -o Read_Sym.o Read_Sym.S

clean:
	rm -f c-as Read_Sym.lst Read_Sym.o Sum.lst Sum.o