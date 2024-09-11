#include "rational.h"
#include "rat_math.c"
#include "rat_io.c"
#include <stdio.h>
#include <string.h>

int main() {
    char input[100];
    rational_t last_result = {0, 1};

    while (fgets(input, sizeof(input), stdin)) {
        char op;
        char num1[50], num2[50];
        sscanf(input, "%s %c %s", num1, &op, num2);

        rational_t a = strcmp(num1, "last") == 0 ? last_result : rat_parse(num1);
        rational_t b = strcmp(num2, "last") == 0 ? last_result : rat_parse(num2);
        rational_t result;

        switch (op) {
            case '+': result = rat_add(a, b); break;
            case '-': result = rat_sub(a, b); break;
            case '*': result = rat_mul(a, b); break;
            case '/': result = rat_div(a, b); break;
            default: continue;
        }

        last_result = result;
        printf("= ");
        rat_print(result);
    }

    return 0;
}
