#include "vm.h"

#ifndef VM_COMMANDS_H
#define VM_COMMANDS_H


#define OP_NONE   0

#define OP_MOV    1
#define OP_SET    2

#define OP_CMP    11
#define OP_TEST   12

#define OP_JMP    21
#define OP_JE     22
#define OP_JNE    23
#define OP_JG     24
#define OP_JGE    25
#define OP_JL     26
#define OP_JLE    27

#define OP_NOT    31
#define OP_AND    32
#define OP_OR     33
#define OP_XOR    34
#define OP_NEG    35

#define OP_INC    41
#define OP_DEC    42

#define OP_ADD    51
#define OP_SUB    52
#define OP_MUL    53
#define OP_DIV    54

#define OP_LOOP   61

#define OP_CALL   71
#define OP_RET    72

#define OP_PUSH   81
#define OP_POP    82

#define OP_NOP    91

#define OP_SYS    101


#define REG_AX   -1
#define REG_BX   -2
#define REG_CX   -3
#define REG_DX   -4

#define REG_SP   -5
#define REG_BP   -6


int h_op_mov(vm_state_t* vm_state);
int h_op_set(vm_state_t* vm_state);

int h_op_cmp(vm_state_t* vm_state);
int h_op_test(vm_state_t* vm_state);

int h_op_jmp(vm_state_t* vm_state);
int h_op_je(vm_state_t* vm_state);
int h_op_jne(vm_state_t* vm_state);
int h_op_jg(vm_state_t* vm_state);
int h_op_jge(vm_state_t* vm_state);
int h_op_jl(vm_state_t* vm_state);
int h_op_jle(vm_state_t* vm_state);

int h_op_not(vm_state_t* vm_state);
int h_op_and(vm_state_t* vm_state);
int h_op_or(vm_state_t* vm_state);
int h_op_xor(vm_state_t* vm_state);
int h_op_neg(vm_state_t* vm_state);

int h_op_inc(vm_state_t* vm_state);
int h_op_dec(vm_state_t* vm_state);

int h_op_add(vm_state_t* vm_state);
int h_op_sub(vm_state_t* vm_state);
int h_op_mul(vm_state_t* vm_state);
int h_op_div(vm_state_t* vm_state);

int h_op_loop(vm_state_t* vm_state);

int h_op_call(vm_state_t* vm_state);
int h_op_ret(vm_state_t* vm_state);

int h_op_push(vm_state_t* vm_state);
int h_op_pop(vm_state_t* vm_state);

int h_op_nop(vm_state_t* vm_state);

int h_op_sys(vm_state_t* vm_state);


#endif
