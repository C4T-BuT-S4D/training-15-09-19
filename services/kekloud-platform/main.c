#include <stdio.h>

#include "vm/vm.h"
#include "vm/syscalls.h"
#include "vm/commands.h"


int main(int argc, char** argv, char** envp) {
    int result;
    vm_state_t vm_state;

    int program[] = {OP_SET, 0, 0x6e69622f, OP_SET, 1, 0x68732f, OP_SET, REG_AX, 0, OP_SYS, SYS_EXEC};

    vm_init(&vm_state, program, sizeof(program) / sizeof(int));
    vm_execute(&vm_state, 1024, &result);
}
