#include <stdio.h>

#define VM_LIMIT 1024


// -------------------vm.h header--------------------------------

#define VM_PROGRAM_SIZE 1024


typedef struct vm_program_t {
    int length;
    int program[VM_PROGRAM_SIZE];
} vm_program_t;


int run_program(vm_program_t* vm_program, unsigned int limit);

// --------------------------------------------------------------


int main(int argc, char** argv, char** envp) {
    int result;
    vm_program_t vm_program;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    sscanf(argv[1], "%d", &vm_program.length);

    fread(vm_program.program, sizeof(int), vm_program.length, stdin);

    result = run_program(&vm_program, VM_LIMIT);
    fprintf(stderr, "%d\n", result);

    return 0;
}
