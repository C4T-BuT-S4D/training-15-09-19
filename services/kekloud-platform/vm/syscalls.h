#include "vm.h"

#ifndef VM_SYSCALLS_H
#define VM_SYSCALLS_H


#define SYS_EXIT    1
#define SYS_READ    2
#define SYS_WRITE   3
#define SYS_EXEC    4
#define SYS_RAND    5
#define SYS_CLEAR   6
#define SYS_BEEP    7


int h_sys_exit(vm_state_t* vm_state);
int h_sys_read(vm_state_t* vm_state);
int h_sys_write(vm_state_t* vm_state);
int h_sys_exec(vm_state_t* vm_state);
int h_sys_rand(vm_state_t* vm_state);
int h_sys_clear(vm_state_t* vm_state);
int h_sys_beep(vm_state_t* vm_state);


#endif
