#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command> [args...]\n", argv[0]);
        return 1;
    }
    execvp(argv[1], &argv[1]);
    perror("execvp"); // If execvp fails, this line is executed
    return 1;
}
