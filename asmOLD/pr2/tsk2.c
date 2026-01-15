#include <stdio.h>

int main()
{
    int eax = 5;
    int ebx = 1;

    while (eax != 0) 
    {
        ebx *= eax;
        eax--;
    }

    return 0;
}
