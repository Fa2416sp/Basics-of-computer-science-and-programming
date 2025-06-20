#include<stdio.h>

int addone(int x){
    return x + 1;
}

int* changemas(int* x){
    for(int i = 0; i < 4; i++){
	x[i] += 1;
    }
    return x;
}
