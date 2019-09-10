#ifndef VM_H
#define VM_H


#define EXEC_SUCCESS               0
#define EXEC_INTERRUPTED           1

#define EXEC_ERR_EXCEEDED_LIMIT   -1
#define EXEC_ERR_INVALID_OP       -2
#define EXEC_ERR_INVALID_ARG      -3
#define EXEC_ERR_SYS_INVALID_OP   -4
#define EXEC_ERR_SYS_INVALID_ARG  -5
#define EXEC_ERR_STACK_OVERFLOW   -6
#define EXEC_ERR_UNKNOWN          -7

#define PROGRAM_SIZE    1024
#define DATA_SIZE       1024
#define STACK_SIZE      1024


typedef struct vm_reg_t {
    unsigned int IP;
    unsigned int SP;
    unsigned int BP;
    unsigned char FLAGS;
    int AX;
    int BX;
    int CX;
    int DX;
} vm_reg_t;

typedef struct vm_mem_t {
    int program[PROGRAM_SIZE];
    int data[DATA_SIZE];
    int stack[STACK_SIZE];
} vm_mem_t;

typedef struct vm_state_t {
    vm_reg_t vm_reg;
    vm_mem_t vm_mem;
} vm_state_t;


void vm_init(vm_state_t* vm_state, int* program, unsigned int length);
void vm_execute(vm_state_t* vm_state, unsigned int limit, int* result);


#endif
