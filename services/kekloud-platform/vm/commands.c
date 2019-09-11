#include <stdio.h>

#include "vm.h"
#include "flags.h"
#include "commands.h"
#include "syscalls.h"


int* _h_get_reg_ptr(vm_state_t* vm_state, int reg) {
    switch (reg) {
        case REG_AX:
            return &vm_state->vm_reg.AX;
        case REG_BX:
            return &vm_state->vm_reg.BX;
        case REG_CX:
            return &vm_state->vm_reg.CX;
        case REG_DX:
            return &vm_state->vm_reg.DX;
        case REG_SP:
            return (int*)&vm_state->vm_reg.SP;
        case REG_BP:
            return (int*)&vm_state->vm_reg.BP;
        default:
            return NULL;
    }
}

int* _h_get_ptr(vm_state_t* vm_state, int address) {
    if (address >= DATA_SIZE)
        return NULL;

    if (address >= 0)
        return &vm_state->vm_mem.data[address];

    return _h_get_reg_ptr(vm_state, address);
}

int h_op_mov(vm_state_t* vm_state) {
    int* src;
    int* dst;

    src = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (src == NULL || dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    *src = *dst;
    vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_set(vm_state_t* vm_state) {
    int* src;

    src = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    
    if (src == NULL)
        return EXEC_ERR_INVALID_ARG;

    *src = vm_state->vm_mem.program[++vm_state->vm_reg.IP];
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_cmp(vm_state_t* vm_state) {
    int result;
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    result = *val1 - *val2;

    if (result == 0)
        vm_state->vm_reg.FLAGS |= FLAG_ZF;
    else
        vm_state->vm_reg.FLAGS &= ~FLAG_ZF;

    if (result < 0)
        vm_state->vm_reg.FLAGS |= FLAG_SF;
    else
        vm_state->vm_reg.FLAGS &= ~FLAG_SF;

    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_test(vm_state_t* vm_state) {
    int result;
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    result = *val1 & *val2;

    if (result == 0)
        vm_state->vm_reg.FLAGS |= FLAG_ZF;
    else
        vm_state->vm_reg.FLAGS &= ~FLAG_ZF;

    vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_jmp(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    vm_state->vm_reg.IP = *dst;

    return EXEC_SUCCESS;
}

int h_op_je(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if ((vm_state->vm_reg.FLAGS & FLAG_ZF) != 0)
        vm_state->vm_reg.IP = *dst;
    else
        vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_jne(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if ((vm_state->vm_reg.FLAGS & FLAG_ZF) == 0)
        vm_state->vm_reg.IP = *dst;
    else
        vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_jg(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if ((vm_state->vm_reg.FLAGS & FLAG_ZF) == 0 && (vm_state->vm_reg.FLAGS & FLAG_SF) == 0)
        vm_state->vm_reg.IP = *dst;
    else
        vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_jge(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if ((vm_state->vm_reg.FLAGS & FLAG_ZF) != 0 || (vm_state->vm_reg.FLAGS & FLAG_SF) == 0)
        vm_state->vm_reg.IP = *dst;
    else
        vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_jl(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if ((vm_state->vm_reg.FLAGS & FLAG_ZF) == 0 && (vm_state->vm_reg.FLAGS & FLAG_SF) != 0)
        vm_state->vm_reg.IP = *dst;
    else
        vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_jle(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if ((vm_state->vm_reg.FLAGS & FLAG_ZF) != 0 || (vm_state->vm_reg.FLAGS & FLAG_SF) != 0)
        vm_state->vm_reg.IP = *dst;
    else
        vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_not(vm_state_t* vm_state) {
    int* val;

    val = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val = ~(*val);
    vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_and(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 & *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_or(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 | *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_xor(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 ^ *val2;

    vm_state->vm_reg.IP++;
    return EXEC_SUCCESS;
}

int h_op_neg(vm_state_t* vm_state) {
    int* val;

    val = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    
    if (val == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val = -(*val);

    vm_state->vm_reg.IP++;
    return EXEC_SUCCESS;
}

int h_op_inc(vm_state_t* vm_state) {
    int* val;

    val = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    
    if (val == NULL)
        return EXEC_ERR_INVALID_ARG;

    (*val)++;

    vm_state->vm_reg.IP++;
    return EXEC_SUCCESS;
}

int h_op_dec(vm_state_t* vm_state) {
    int* val;

    val = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    
    if (val == NULL)
        return EXEC_ERR_INVALID_ARG;

    (*val)--;

    vm_state->vm_reg.IP++;
    return EXEC_SUCCESS;
}

int h_op_add(vm_state_t* vm_state) {
    int* val1;
    int *val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 + *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_sub(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 - *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_mul(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 * *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_div(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 / *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_mod(vm_state_t* vm_state) {
    int* val1;
    int* val2;

    val1 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);
    val2 = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (val1 == NULL || val2 == NULL)
        return EXEC_ERR_INVALID_ARG;

    *val1 = *val1 % *val2;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_loop(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if (vm_state->vm_reg.CX > 0) {
        vm_state->vm_reg.CX--;
        vm_state->vm_reg.IP = *dst;
    }
    else {
        vm_state->vm_reg.IP++;
    }

    return EXEC_SUCCESS;
}

int h_op_call(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (*dst < 0 || *dst >= PROGRAM_SIZE)
        return EXEC_ERR_INVALID_ARG;

    if (vm_state->vm_reg.SP >= STACK_SIZE)
        return EXEC_ERR_STACK_OVERFLOW;

    vm_state->vm_mem.stack[vm_state->vm_reg.SP++] = vm_state->vm_reg.IP + 1;
    vm_state->vm_reg.IP = *dst;
    
    return EXEC_SUCCESS;
}

int h_op_ret(vm_state_t* vm_state) {
    if (vm_state->vm_reg.SP <= 0)
        return EXEC_ERR_STACK_OVERFLOW;

    vm_state->vm_reg.IP = vm_state->vm_mem.stack[--vm_state->vm_reg.SP];
    
    return EXEC_SUCCESS;
}

int h_op_push(vm_state_t* vm_state) {
    int* src;

    src = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (src == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (vm_state->vm_reg.SP >= STACK_SIZE)
        return EXEC_ERR_STACK_OVERFLOW;

    vm_state->vm_mem.stack[vm_state->vm_reg.SP++] = *src;
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_pop(vm_state_t* vm_state) {
    int* dst;

    dst = _h_get_ptr(vm_state, vm_state->vm_mem.program[++vm_state->vm_reg.IP]);

    if (dst == NULL)
        return EXEC_ERR_INVALID_ARG;

    if (vm_state->vm_reg.SP <= 0)
        return EXEC_ERR_STACK_OVERFLOW;

    *dst = vm_state->vm_mem.stack[--vm_state->vm_reg.SP];
    vm_state->vm_reg.IP++;

    return EXEC_SUCCESS;
}

int h_op_nop(vm_state_t* vm_state) {
    vm_state->vm_reg.IP++;
    
    return EXEC_SUCCESS;
}

int h_op_sys(vm_state_t* vm_state) {
    int result;

    switch (vm_state->vm_mem.program[++vm_state->vm_reg.IP]) {
        case SYS_EXIT:
            result = h_sys_exit(vm_state);
            break;
        case SYS_READ:
            result = h_sys_read(vm_state);
            break;
        case SYS_WRITE:
            result = h_sys_write(vm_state);
            break;
        case SYS_EXEC:
            result = h_sys_exec(vm_state);
            break;
        case SYS_RAND:
            result = h_sys_rand(vm_state);
            break;
        case SYS_CLEAR:
            result = h_sys_clear(vm_state);
            break;
        case SYS_BEEP:
            result = h_sys_beep(vm_state);
            break;
        default:
            result = EXEC_ERR_SYS_INVALID_OP;
            break;
    }

    vm_state->vm_reg.IP++;
    
    return result;
}
