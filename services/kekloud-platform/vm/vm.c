#include <string.h>

#include "vm.h"
#include "commands.h"


void vm_init(vm_state_t* vm_state, int* program, unsigned int length) {
    vm_state->vm_reg.IP = 0;
    vm_state->vm_reg.SP = 0;
    vm_state->vm_reg.BP = 0;
    vm_state->vm_reg.FLAGS = 0;

    vm_state->vm_reg.AX = 0;
    vm_state->vm_reg.BX = 0;
    vm_state->vm_reg.CX = 0;
    vm_state->vm_reg.DX = 0;

    memset(vm_state->vm_mem.program, 0, VM_PROGRAM_SIZE * sizeof(int));
    memset(vm_state->vm_mem.data, 0, VM_DATA_SIZE * sizeof(int));
    memset(vm_state->vm_mem.stack, 0, VM_STACK_SIZE * sizeof(int));
    
    memcpy(vm_state->vm_mem.program, program, length * sizeof(int));
}

void vm_execute(vm_state_t* vm_state, unsigned int limit, int* result) {
    int ops_count;

    ops_count = 0;

    while (vm_state->vm_mem.program[vm_state->vm_reg.IP] != OP_NONE) {
        switch (vm_state->vm_mem.program[vm_state->vm_reg.IP]) {
            case OP_MOV:
                *result = h_op_mov(vm_state);
                break;
            case OP_SET:
                *result = h_op_set(vm_state);
                break;
            case OP_CMP:
                *result = h_op_cmp(vm_state);
                break;
            case OP_TEST:
                *result = h_op_test(vm_state);
                break;
            case OP_JMP:
                *result = h_op_jmp(vm_state);
                break;
            case OP_JE:
                *result = h_op_je(vm_state);
                break;
            case OP_JNE:
                *result = h_op_jne(vm_state);
                break;
            case OP_JG:
                *result = h_op_jg(vm_state);
                break;
            case OP_JGE:
                *result = h_op_jge(vm_state);
                break;
            case OP_JL:
                *result = h_op_jl(vm_state);
                break;
            case OP_JLE:
                *result = h_op_jle(vm_state);
                break;
            case OP_NOT:
                *result = h_op_not(vm_state);
                break;
            case OP_AND:
                *result = h_op_and(vm_state);
                break;
            case OP_OR:
                *result = h_op_or(vm_state);
                break;
            case OP_XOR:
                *result = h_op_xor(vm_state);
                break;
            case OP_NEG:
                *result = h_op_neg(vm_state);
                break;
            case OP_INC:
                *result = h_op_inc(vm_state);
                break;
            case OP_DEC:
                *result = h_op_dec(vm_state);
                break;
            case OP_ADD:
                *result = h_op_add(vm_state);
                break;
            case OP_SUB:
                *result = h_op_sub(vm_state);
                break;
            case OP_MUL:
                *result = h_op_mul(vm_state);
                break;
            case OP_DIV:
                *result = h_op_div(vm_state);
                break;
            case OP_MOD:
                *result = h_op_div(vm_state);
                break;
            case OP_LOOP:
                *result = h_op_loop(vm_state);
                break;
            case OP_CALL:
                *result = h_op_call(vm_state);
                break;
            case OP_RET:
                *result = h_op_ret(vm_state);
                break;
            case OP_PUSH:
                *result = h_op_push(vm_state);
                break;
            case OP_POP:
                *result = h_op_pop(vm_state);
                break;
            case OP_NOP:
                *result = h_op_nop(vm_state);
                break;
            case OP_SYS:
                *result = h_op_sys(vm_state);
                break;
            default:
                *result = EXEC_ERR_INVALID_OP;
                break;
        }

        ops_count++;

        if (ops_count >= limit) {
            *result = EXEC_ERR_EXCEEDED_LIMIT;
            break;
        }

        if (*result == EXEC_INTERRUPTED) {
            *result = vm_state->vm_reg.AX;
            break;
        }

        if (*result != EXEC_SUCCESS)
            break;
    }
}

void vm_run(int* program, unsigned int length, unsigned int limit, int* result) {
    vm_state_t vm_state;

    vm_init(&vm_state, program, length);
    vm_execute(&vm_state, limit, result);
}

int run_program(int* program, unsigned int length, unsigned int limit) {
    int result;

    if (length >= VM_PROGRAM_SIZE)
        return EXEC_ERR_PROGRAM_TOO_LONG;

    vm_run(program, length, limit, &result);

    return result;
}
