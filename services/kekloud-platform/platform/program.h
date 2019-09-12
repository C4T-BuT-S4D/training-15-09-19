#ifndef KPL_PROGRAM_H
#define KPL_PROGRAM_H

#include "vm.h"
#include "account.h"


#define DIR_MACHINES "machines"


typedef struct vm_program_t {
    int length;
    int program[VM_PROGRAM_SIZE];
} vm_program_t;


int save_program(vm_program_t* vm_program, vm_account_t* vm_account);
int load_program(vm_program_t* vm_program, vm_account_t* vm_account);
int read_program(vm_program_t* vm_program);
int list_programs();


#endif
