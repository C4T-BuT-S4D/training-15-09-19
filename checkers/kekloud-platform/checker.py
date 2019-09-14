#!/usr/bin/env python3

import sys
import socket

from helpers import FlagInfo, SocketIO
from checklib import Status, cquit, rnd_string
from generators import generate_simple, generate_encrypted, generate_checking


PORT    = 7002
TIMEOUT = 10

VULN_SIMPLE    = '1'
VULN_ENCRYPTED = '2'

BANNER = b'\x20\x5f\x5f\x20\x20\x5f\x5f\x5f\x20\x20\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x20\x20\x5f\x5f\x20\x20\x5f\x5f\x5f\x20\x20\x5f\x5f\x20\x20\x20\x20\x20\x20\x20\x20\x5f\x5f\x5f\x5f\x5f\x5f\x20\x20\x20\x20\x5f\x5f\x20\x20\x20\x20\x5f\x5f\x20\x20\x20\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x20\x20\x0a\x7c\x20\x20\x7c\x2f\x20\x20\x2f\x20\x7c\x20\x20\x20\x5f\x5f\x5f\x5f\x7c\x7c\x20\x20\x7c\x2f\x20\x20\x2f\x20\x7c\x20\x20\x7c\x20\x20\x20\x20\x20\x20\x2f\x20\x20\x5f\x5f\x20\x20\x5c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x20\x20\x20\x20\x20\x5c\x20\x0a\x7c\x20\x20\x27\x20\x20\x2f\x20\x20\x7c\x20\x20\x7c\x5f\x5f\x20\x20\x20\x7c\x20\x20\x27\x20\x20\x2f\x20\x20\x7c\x20\x20\x7c\x20\x20\x20\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x2e\x2d\x2d\x2e\x20\x20\x7c\x0a\x7c\x20\x20\x20\x20\x3c\x20\x20\x20\x7c\x20\x20\x20\x5f\x5f\x7c\x20\x20\x7c\x20\x20\x20\x20\x3c\x20\x20\x20\x7c\x20\x20\x7c\x20\x20\x20\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x0a\x7c\x20\x20\x2e\x20\x20\x5c\x20\x20\x7c\x20\x20\x7c\x5f\x5f\x5f\x5f\x20\x7c\x20\x20\x2e\x20\x20\x5c\x20\x20\x7c\x20\x20\x60\x2d\x2d\x2d\x2d\x2e\x7c\x20\x20\x60\x2d\x2d\x27\x20\x20\x7c\x20\x7c\x20\x20\x60\x2d\x2d\x27\x20\x20\x7c\x20\x7c\x20\x20\x27\x2d\x2d\x27\x20\x20\x7c\x0a\x7c\x5f\x5f\x7c\x5c\x5f\x5f\x5c\x20\x7c\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x7c\x7c\x5f\x5f\x7c\x5c\x5f\x5f\x5c\x20\x7c\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x7c\x20\x5c\x5f\x5f\x5f\x5f\x5f\x5f\x2f\x20\x20\x20\x5c\x5f\x5f\x5f\x5f\x5f\x5f\x2f\x20\x20\x7c\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x2f\x20\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20'.replace(b'\n', b'')


def check(host):
    program, length, output, code = generate_checking()

    io = SocketIO(host, PORT, TIMEOUT)

    try:
        # banner
        if b''.join(io.recvlines(7)) != BANNER:
            cquit(Status.MUMBLE, 'Logo was changed')
        # main menu (Create VM)
        io.recvlines(4)
        io.sendline(b'1')
        # send length
        io.recvline()
        io.sendline(str(length).encode())
        # send program
        io.recvline()
        io.send(program)
        # run menu (Yes)
        io.recvlines(4)
        io.sendline(b'1')
        # checking output
        result = io.recvline()
        if output.strip() != result.strip().decode():
            cquit(Status.MUMBLE, 'Invalid checking value')
        result = io.recvline()
        if f'code {code}' not in result:
            cquit(Status.MUMBLE, 'Invalid checking code')
        # save vm (Yes)
        io.recvlines(3)
        io.sendline(b'1')
        if b'saved' not in io.recvline():
            cquit(Status.MUMBLE, 'VM can not be saved')
        # get vm info
        vm_name = io.recvline()[10:].decode()
        vm_password = io.recvline()[14:].decode()
        # bye
        io.recvline()
    except Exception as e:
        cquit(Status.MUMBLE, 'Error while checking flag', f'Error while checking flag: {str(e)}')
    finally:
        io.close()

    flag_info = FlagInfo(vm_name, vm_password)

    io = SocketIO(host, PORT, TIMEOUT)

    try:
        # banner
        if b''.join(io.recvlines(7)) != BANNER:
            cquit(Status.MUMBLE, 'Logo was changed')
        # main menu (List VMs)
        io.recvlines(4)
        io.sendline(b'3')
        # reading names
        vm_names = []
        while True:
            vm_name = io.recvline()
            if b'Create VM' in vm_name:
                break
            vm_names.append(vm_name.decode())
        # checking vm existing
        if flag_info.vm_name not in vm_names:
            cquit(Status.MUMBLE, 'VM not found', f'VM not found, vuln: {vuln}')
        # main menu (Load VM)
        io.recvlines(3)
        io.sendline(b'2')
        # send vm info
        io.recvline()
        io.sendline(flag_info.vm_name.encode())
        if 'Invalid character' in io.recvline():
            cquit(Status.MUMBLE, 'Name does not require restrictions')
        io.sendline(flag_info.vm_password.encode())
        answer = io.recvline()
        if b'Invalid character' in answer:
            cquit(Status.MUMBLE, 'Password does not require restrictions')
        if b'Invalid password' in answer:
            cquit(Status.MUMBLE, 'Invalid password')
        if b'Program loaded' not in answer:
            cquit(Status.CORRUPT, 'VM can not be loaded')
        # run vm (Yes)
        io.recvlines(3)
        io.sendline(b'1')
        # checking output
        result = io.recvline()
        if output.strip() != result.strip().decode():
            cquit(Status.MUMBLE, 'Invalid checking value')
        result = io.recvline()
        if f'code {code}'.encode() not in result:
            cquit(Status.MUMBLE, 'Invalid checking code')
        # save vm (No)
        io.recvlines(3)
        io.sendline(b'2')
        # bye
        io.recvline()
    except Exception as e:
        cquit(Status.MUMBLE, 'Error while checking flag', f'Error while checking flag: {str(e)}')
    finally:
        io.close()


def put(host, flag_id, flag, vuln):
    if vuln == VULN_SIMPLE:
        flag_password = None
        program, length = generate_simple(flag)
    elif vuln == VULN_ENCRYPTED:
        flag_password = rnd_string(16)
        program, length = generate_encrypted(flag, flag_password)
    else:
        cquit(Status.ERROR, 'System error', f'Vuln number {vuln} is unknown')

    io = SocketIO(host, PORT, TIMEOUT)

    try:
        # banner
        if b''.join(io.recvlines(7)) != BANNER:
            cquit(Status.MUMBLE, 'Logo was changed')
        # main menu (Create VM)
        io.recvlines(4)
        io.sendline(b'1')
        # send length
        io.recvline()
        io.sendline(str(length).encode())
        # send program
        io.recvline()
        io.send(program)
        # run menu (No)
        io.recvlines(4)
        io.sendline(b'2')
        # save menu (Yes)
        io.recvlines(3)
        io.sendline(b'1')
        if b'saved' not in io.recvline():
            cquit(Status.MUMBLE, 'VM can not be saved')
        # get vm info
        vm_name = io.recvline()[10:].decode()
        vm_password = io.recvline()[14:].decode()
        # bye
        io.recvline()
    except Exception as e:
        cquit(Status.MUMBLE, 'Error while putting flag', f'Error while putting flag: {str(e)}, vuln: {vuln}')
    finally:
        io.close()

    flag_info = FlagInfo(vm_name, vm_password, flag_password)

    cquit(Status.OK, flag_info.dump())


def get(host, flag_id, flag, vuln):
    if vuln not in [VULN_SIMPLE, VULN_ENCRYPTED]:
        cquit(Status.ERROR, 'System error', f'Vuln number {vuln} is unknown')

    flag_info = FlagInfo.load(flag_id)

    io = SocketIO(host, PORT, TIMEOUT)

    try:
        # banner
        if b''.join(io.recvlines(7)) != BANNER:
            cquit(Status.MUMBLE, 'Logo was changed')
        # main menu (List VMs)
        io.recvlines(4)
        io.sendline(b'3')
        # reading names
        vm_names = []
        while True:
            vm_name = io.recvline()
            if b'Create VM' in vm_name:
                break
            vm_names.append(vm_name.decode())
        # checking vm existing
        if flag_info.vm_name not in vm_names:
            cquit(Status.CORRUPT, 'VM not found', f'VM not found, vuln: {vuln}')
        # main menu (Load VM)
        io.recvlines(3)
        io.sendline(b'2')
        # send vm info
        io.recvline()
        io.sendline(flag_info.vm_name.encode())
        if b'Invalid character' in io.recvline():
            cquit(Status.MUMBLE, 'Name does not require restrictions')
        io.sendline(flag_info.vm_password.encode())
        answer = io.recvline()
        if b'Invalid character' in answer:
            cquit(Status.MUMBLE, 'Password does not require restrictions')
        if b'Invalid password' in answer:
            cquit(Status.MUMBLE, 'Invalid password')
        if b'Program loaded' not in answer:
            cquit(Status.CORRUPT, 'VM can not be loaded')
        # run vm (Yes)
        io.recvlines(3)
        io.sendline(b'1')
        # get flag
        message = io.recvline()
        if b'VM exited' in message:
            cquit(Status.MUMBLE, 'VM does not work as expected', f'VM does not work as expected: {message}')
        if int(b'protected' in message) ^ int(vuln == VULN_ENCRYPTED):
            cquit(Status.CORRUPT, 'Password requirements does not match', f'Password requirements does not match, vuln: {vuln}')
        if b'protected' in message:
            io.sendline(flag_info.flag_password.encode())
        result = io.recvline()
        if b'No!' in result:
            cquit(Status.MUMBLE, 'Invalid password', f'Invalid password, expected: {flag_id.flag_password}')
        if flag.strip() not in result.strip().decode():
            cquit(Status.CORRUPT, 'Invalid flag', f'Invalid flag, expected: {flag}, actual: {result}, vuln: {vuln}')
        #read vm code
        code = io.recvline()[4:]
        if b'code 0' not in code:
            cquit(Status.MUMBLE, 'VM does not work as expected', f'VM does not work as expected: {code}')
        # bye
        io.recvline()
    except Exception as e:
        cquit(Status.MUMBLE, 'Error while getting flag', f'Error while getting flag: {str(e)}, vuln: {vuln}')
    finally:
        io.close()

    cquit(Status.OK)


if __name__ == '__main__':
    action, *args = sys.argv[1:]

    try:
        if action == 'check':
            host, = args
            check(host)

        elif action == 'put':
            host, flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)

        elif action == 'get':
            host, flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)

        else:
            cquit(Status.ERROR, 'System error', f'Unknown action: {action}')

        cquit(Status.ERROR, 'System error', f'Action {action} ended without cquit')

    except socket.error as e:
        cquit(Status.DOWN, 'Connection error', f'Connection error: {str(e)}')

    except socket.timeout as e:
        cquit(Status.DOWN, 'Connection timeout', f'Connection timeout: {str(e)}')

    except Exception as e:
        cquit(Status.ERROR, 'System error', f'Unhandled exception: {str(e)}')
