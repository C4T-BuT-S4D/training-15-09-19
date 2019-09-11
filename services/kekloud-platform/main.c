#include <stdio.h>

#include "vm/vm.h"
#include "vm/syscalls.h"
#include "vm/commands.h"


int exploit_1[] = {OP_SET, 0, 0x6e69622f, OP_SET, 1, 0x0068732f, OP_SYS, SYS_EXEC};


int main(int argc, char** argv, char** envp) {
    int result;
    vm_state_t vm_state;

    int program[] = {};

    vm_init(&vm_state, program, sizeof(program) / sizeof(int));
    vm_execute(&vm_state, 1024, &result);

    printf("%d %d %d\n", result, vm_state.vm_reg.AX, vm_state.vm_reg.BX);

    return 0;
}
