#include <stdio.h>

#include "vm/vm.h"
#include "vm/commands.h"


int main(int argc, char** argv, char** envp) {
    int result;
    vm_state_t vm_state;

    int program[] = {OP_SET, REG_AX, 1337, OP_PUSH, REG_AX, OP_INC, REG_AX, OP_POP, REG_AX};

    vm_init(&vm_state, program, sizeof(program) / sizeof(int));
    vm_execute(&vm_state, 1024, &result);

    printf("%d\n", vm_state.vm_reg.AX);
}
