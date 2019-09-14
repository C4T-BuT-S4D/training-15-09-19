#!/usr/bin/env python3

import os
import re

from struct import pack, unpack
from random import shuffle, randint, choice
from subprocess import Popen, PIPE

from constants import *


SIMPLE_MESSAGES = [
    'just a flag for you:\n',
    'sorry, no encryption today\n',
    'ez pz srvc flg\n',
    'keks were here\n',
    'by C4T BuT S4D with love <3\n',
    'does ker mean haker?\n',
    'how did you see this?\rwelcome to our training\n'
]

ENCRYPTED_MESSAGE = 'Flag is protected! Input password:\n'
ENCRYPTED_FAIL    = 'No!\n'


def rand():
    return randint(-(1<<31), 1<<31 - 1)


def randl(n=31):
    return rand() % (1 << n)


def rand2():
    return bool(rand() % 2)


def pads(s):
    return s + '\x00' * (-len(s) % 4)


def pack_long(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000


def pack_str(s):
    return list(unpack('<' + 'i' * (len(s)//4), s.encode()))


def pack_program(program):
    return b''.join(pack('<i', pack_long(c)) for c in program)


def put_data(program, data, offset):
    enum = list(enumerate(data))
    shuffle(enum)
    for i, n in enum:
        if rand2():
            program.extend([OP_SET, offset + i, n])
        else:
            reg = choice([REG_AX, REG_BX, REG_CX, REG_DX])
            program.extend([
                OP_SET, reg, n,
                OP_MOV, offset + i, reg
            ])


def multibyte_xor(program, offset1, offset2, length):
    program.extend([
        OP_SET, 1000, len(program) + 6,
        OP_SET, REG_CX, length - 1
    ])
    enum = list(range(length))
    shuffle(enum)
    for i in enum:
        program.extend([
            OP_MOV, REG_AX, offset1 + i,
            OP_MOV, REG_BX, offset2 + i,
            OP_XOR, REG_AX, REG_BX,
            OP_MOV, offset1 + i, REG_AX,
            OP_LOOP, 1000
        ])


def compare_data(program, offset1, offset2, length, error_str_offset, error_str_length):
    program.extend([
        OP_SET, 1001, len(program) + 8,
        OP_SET, 1002, len(program) + 21,
        OP_JMP, 1002,
        OP_SET, REG_AX, error_str_offset,
        OP_SET, REG_BX, error_str_length,
        OP_SYS, SYS_WRITE,
        OP_SET, REG_AX, -1,
        OP_SYS, SYS_EXIT
        ])
    program.extend([
        OP_SET, 1000, len(program) + 6,
        OP_SET, REG_CX, length - 1
    ])
    enum = list(range(length))
    shuffle(enum)
    for i in enum:
        program.extend([
            OP_MOV, REG_AX, offset1 + i,
            OP_MOV, REG_BX, offset2 + i,
            OP_CMP, REG_AX, REG_BX,
            OP_JNE, 1001,
            OP_LOOP, 1000
        ])


def generate_simple(flag):
    flag_offset = 100
    message_offset = 200
    key_offset = 300
    program = []
    flag += '\n'
    flag_length = len(flag)
    flag = pack_str(pads(flag))
    message = choice(SIMPLE_MESSAGES)
    message_length = len(message)
    message = pack_str(pads(message))
    key = [rand() for i in range(len(flag))]
    xored = [f^k for f,k in zip(flag, key)]
    put_data(program, xored, flag_offset)
    put_data(program, message, message_offset)
    put_data(program, key, key_offset)
    multibyte_xor(program, flag_offset, key_offset, len(flag))
    program.extend([
        OP_SET, REG_AX, message_offset,
        OP_SET, REG_BX, message_length,
        OP_SYS, SYS_WRITE,
        OP_SET, REG_AX, flag_offset,
        OP_SET, REG_BX, flag_length,
        OP_SYS, SYS_WRITE,
        OP_SET, REG_AX, 0,
        OP_SYS, SYS_EXIT
    ])
    return pack_program(program), len(program)


def generate_encrypted(flag, password):
    flag_offset = 100
    password_offset = 200
    message_offset = 300
    error_offset = 400
    input_offset = 500
    program = []
    flag += '\n'
    flag_length = len(flag)
    flag = pack_str(pads(flag))
    password_length = len(password)
    password = pack_str(pads(password))
    message_length = len(ENCRYPTED_MESSAGE)
    message = pack_str(pads(ENCRYPTED_MESSAGE))
    error_length = len(ENCRYPTED_FAIL)
    error = pack_str(pads(ENCRYPTED_FAIL))
    input_length = password_length * 2
    put_data(program, password, password_offset)
    put_data(program, message, message_offset)
    put_data(program, error, error_offset)
    program.extend([
        OP_SET, REG_AX, message_offset,
        OP_SET, REG_BX, message_length,
        OP_SYS, SYS_WRITE,
        OP_SET, REG_AX, input_offset,
        OP_SET, REG_BX, input_length,
        OP_SYS, SYS_READ
    ])
    compare_data(program, password_offset, input_offset, len(password), error_offset, error_length)
    put_data(program, flag, flag_offset)
    program.extend([
        OP_SET, REG_AX, flag_offset,
        OP_SET, REG_BX, flag_length,
        OP_SYS, SYS_WRITE,
        OP_SET, REG_AX, 0,
        OP_SYS, SYS_EXIT
    ])
    return pack_program(program), len(program)


def get_output(program):
    payload = str(len(program)).encode() + b'\n' + pack_program(program)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    runner_path = os.path.join(base_dir, 'runner')
    process = Popen([runner_path], stdin=PIPE, stdout=PIPE)
    result = process.communicate(payload)[0]
    code = re.findall(rb'\d+', result)[-1]
    return result[:-len(code)-1], code


def generate_checking():
    consts = [abs(randl()) for i in range(8)]
    regs = [REG_AX, REG_BX, REG_CX, REG_DX]
    shuffle(regs)
    val0, val1, val2, val3 = 1000, 1001, 1002, 1003
    program_parts = [
        # je, jne, jg, jge, jl, jle
        [
            OP_SET, regs[0], consts[0],
            OP_SET, regs[1], consts[1],
            OP_SET, regs[2], randl() % VM_PROGRAM_SIZE,
            OP_CMP, regs[0], regs[1],
            OP_JE, regs[2]
        ],
        [
            OP_SET, regs[0], consts[2],
            OP_SET, regs[1], consts[2],
            OP_SET, regs[2], randl() % VM_PROGRAM_SIZE,
            OP_CMP, regs[0], regs[1],
            OP_JNE, regs[2]
        ],
        [
            OP_SET, regs[0], consts[3] // 1337,
            OP_SET, regs[1], consts[3],
            OP_SET, regs[2], randl() % VM_PROGRAM_SIZE,
            OP_CMP, regs[0], regs[1],
            OP_JG, regs[2]
        ],
        [
            OP_SET, regs[0], consts[4] // 1337,
            OP_SET, regs[1], consts[4],
            OP_SET, regs[2], randl() % VM_PROGRAM_SIZE,
            OP_CMP, regs[0], regs[1],
            OP_JGE, regs[2]
        ],
        [
            OP_SET, regs[0], consts[5],
            OP_SET, regs[1], consts[5] // 1337,
            OP_SET, regs[2], randl() % VM_PROGRAM_SIZE,
            OP_CMP, regs[0], regs[1],
            OP_JL, regs[2]
        ],
        [
            OP_SET, regs[0], consts[6],
            OP_SET, regs[1], consts[6] // 1337,
            OP_SET, regs[2], randl() % VM_PROGRAM_SIZE,
            OP_CMP, regs[0], regs[1],
            OP_JLE, regs[2]
        ],
        # not, and, or, xor, neg
        [
            OP_SET, regs[0], randl(),
            OP_NOT, regs[0],
            OP_XOR, val1, regs[0]
        ],
        [
            OP_SET, regs[0], randl(),
            OP_SET, regs[1], randl(),
            OP_AND, regs[0], regs[1],
            OP_XOR, val1, regs[0]
        ],
        [
            OP_SET, regs[0], randl(),
            OP_SET, regs[1], randl(),
            OP_OR, regs[0], regs[1],
            OP_XOR, val1, regs[0]
        ],
        [
            OP_SET, regs[0], randl(),
            OP_SET, regs[1], randl(),
            OP_XOR, regs[0], regs[1],
            OP_XOR, val1, regs[0]
        ],
        [
            OP_SET, regs[0], randl(),
            OP_NEG, regs[0],
            OP_XOR, val1, regs[0]
        ],
        # inc, dec
        [
            OP_SET, regs[1], randl(),
            OP_INC, regs[1],
            OP_XOR, val2, regs[1]
        ],
        [
            OP_SET, regs[1], randl(),
            OP_DEC, regs[1],
            OP_XOR, val2, regs[1]
        ],
        # add, sub, mul, div, mod
        [
            OP_SET, regs[2], randl(),
            OP_SET, regs[3], randl(),
            OP_ADD, regs[2], regs[3],
            OP_XOR, val3, regs[2]
        ],
        [
            OP_SET, regs[2], randl(),
            OP_SET, regs[3], randl(),
            OP_SUB, regs[2], regs[3],
            OP_XOR, val3, regs[2]
        ],
        [
            OP_SET, regs[2], randl(),
            OP_SET, regs[3], randl(),
            OP_MUL, regs[2], regs[3],
            OP_XOR, val3, regs[2]
        ],
        [
            OP_SET, regs[2], randl(),
            OP_SET, regs[3], randl(),
            OP_DIV, regs[2], regs[3],
            OP_XOR, val3, regs[2]
        ],
        [
            OP_SET, regs[2], randl(),
            OP_SET, regs[3], randl(),
            OP_MOD, regs[2], regs[3],
            OP_XOR, val3, regs[2]
        ],
        # push, pop
        [
            OP_SET, regs[0], randl(),
            OP_SET, regs[1], randl(),
            OP_PUSH, regs[0],
            OP_PUSH, regs[1],
            OP_POP, regs[2],
            OP_POP, regs[3],
            OP_XOR, val0, regs[2],
            OP_XOR, val1, regs[3]
        ],
        # nop
        [
            OP_NOP
        ],
        # syscalls
        [
            OP_SYS, SYS_BEEP
        ]
        # [
        #     OP_SYS, SYS_RAND,
        #     OP_XOR, val3, REG_AX
        # ]
    ]
    shuffle(program_parts)
    program = [
        OP_SET, REG_AX, randl(),
        OP_SYS, SYS_CLEAR,
    ]
    for part in program_parts:
        program.extend(part)
    program.extend([
        # loop
        OP_SET, REG_BP, randl(),
        OP_SET, REG_CX, 2,
        OP_SET, 100, len(program) + 9,
        OP_INC, REG_BP,
        OP_LOOP, 100,
        OP_XOR, val0, REG_BP
    ])
    program.extend([
        # call, ret
        OP_SET, 100, len(program) + 11,
        OP_SET, 101, len(program) + 14,
        OP_SET, regs[3], randl(),
        OP_JMP, 101,
        OP_INC, regs[3],
        OP_RET,
        OP_CALL, 100,
        OP_XOR, val0, regs[3]
    ])
    program.extend([
        # write, exit
        OP_SET, REG_AX, val0,
        OP_SET, REG_BX, 16,
        OP_SYS, SYS_WRITE,
        OP_SET, REG_AX, consts[7],
        OP_SYS, SYS_EXIT
    ])
    output, code = get_output(program)
    return pack_program(program), len(program), output, code

