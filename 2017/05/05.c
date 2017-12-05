#include <stdio.h>

#define SIZE 10000

int main() {
    FILE *file;
    int maze[SIZE];
    int times;
    int number;
    int length;
    int pos;
    int steps;
    int inc;

    for(times=0; times<2; times++) {

        // Fill maze
        length = 0;
        file = fopen("input", "r");
        while( fscanf(file, "%d\n", &number) > 0 ) {
            maze[length++] = number;
        }
        fclose(file);

        pos = 0;
        steps = 0;

        while(pos >= 0 && pos < length) {
            inc = 1;
            if(times == 1 && maze[pos] >= 3)
                inc = -1;
            maze[pos] += inc;
            pos += maze[pos] - inc;
            steps += 1;
        }
        printf("%d\n", steps);
    }
}
