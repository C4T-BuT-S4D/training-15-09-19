#!/usr/bin/env python3

from struct import pack, unpack
from random import shuffle, randint, choice
from constants import *


SIMPLE_MESSAGES = [
    'just a flag for you:\n',
    'sorry, no encryption today\n',
    'ez pz srvc flg\n',
    'keks were here\n',
    'by C4T BuT S4D with love <3\n',
    'does ker mean haker?\n',
    'how did you see this?\nwelcome to out training\n'
]

ENCRYPTED_MESSAGE = 'Flag is protected! Input password:\n'
ENCRYPTED_FAIL    = 'No!\n'


def rand():
    return randint(-(1<<31), 1<<31 - 1)


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


def generate_checking():
    pass
