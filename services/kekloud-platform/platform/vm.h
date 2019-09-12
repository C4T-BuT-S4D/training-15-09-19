#ifndef KPL_VM_H
#define KPL_VM_H


#define VM_PROGRAM_SIZE 1024


typedef struct vm_program_t {
    int length;
    int program[VM_PROGRAM_SIZE];
} vm_program_t;


int run_program(vm_program_t* vm_program, unsigned int limit);


#endif
