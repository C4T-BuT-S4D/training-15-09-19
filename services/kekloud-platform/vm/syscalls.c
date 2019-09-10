#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "vm.h"
#include "syscalls.h"


int h_sys_exit(vm_state_t* vm_state) {
    return EXEC_INTERRUPTED;
}

int h_sys_read(vm_state_t* vm_state) {
    if (vm_state->vm_reg.AX < 0 || vm_state->vm_reg.BX < 0 || 
        vm_state->vm_reg.AX + vm_state->vm_reg.BX >= DATA_SIZE)
        return EXEC_ERR_SYS_INVALID_ARG;

    read(0, vm_state->vm_mem.data + vm_state->vm_reg.AX, vm_state->vm_reg.BX);

    return EXEC_SUCCESS;
}

int h_sys_write(vm_state_t* vm_state) {
    if (vm_state->vm_reg.AX < 0 || vm_state->vm_reg.BX < 0 || 
        vm_state->vm_reg.AX + vm_state->vm_reg.BX >= DATA_SIZE)
        return EXEC_ERR_SYS_INVALID_ARG;

    write(1, &vm_state->vm_mem.data[vm_state->vm_reg.AX], vm_state->vm_reg.BX);
    
    return EXEC_SUCCESS;
}

int h_sys_exec(vm_state_t* vm_state) {
    if (vm_state->vm_reg.AX < 0 || vm_state->vm_reg.AX >= DATA_SIZE)
        return EXEC_ERR_SYS_INVALID_ARG;

    __asm__(
        "mov %0, %%rdi;"
        "xor %%rsi, %%rsi;"
        "xor %%rdx, %%rdx;"
        "mov $0x3b, %%rax;"
        "syscall;"
        :
        : "b" (&vm_state->vm_mem.data[vm_state->vm_reg.AX]));

    return EXEC_SUCCESS;
}

int h_sys_rand(vm_state_t* vm_state) {
    FILE* file;

    if ((file = fopen("/dev/urandom", "r")) == NULL)
        return EXEC_ERR_UNKNOWN;

    fread(&vm_state->vm_reg.AX, sizeof(int), 1, file);
    fclose(file);

    return EXEC_SUCCESS;
}

int h_sys_clear(vm_state_t* vm_state) {
    memset(vm_state->vm_mem.data, vm_state->vm_reg.AX, DATA_SIZE);

    return EXEC_SUCCESS;
}

int h_sys_beep(vm_state_t* vm_state) {
    puts("beep!");

    return EXEC_SUCCESS;
}
