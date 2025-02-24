#include <stdio.h>

int main() {
    int x = 10;
    int *p = &x;
    int **p = &p;
    int ***p = &p;
    int ****p = &p;

    char **array = malloc(10 * sizeof(char *));
}

