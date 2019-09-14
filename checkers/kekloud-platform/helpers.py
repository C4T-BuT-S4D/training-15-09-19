#!/usr/bin/env python3

import json
import socket


class FlagInfo(object):
    def __init__(self, vm_name, vm_password, flag_password=None):
        self._vm_name = vm_name
        self._vm_password = vm_password
        self._flag_password = flag_password

    @property
    def vm_name(self):
        return self._vm_name

    @property
    def vm_password(self):
        return self._vm_password

    @property
    def flag_password(self):
        return self._flag_password

    def dump(self):
        return json.dumps({
            'vm_name': self.vm_name,
            'vm_password': self.vm_password,
            'flag_password': self.flag_password
        })

    @classmethod
    def load(self, data):
        return FlagInfo(**json.loads(data))


class SocketIO(object):
    def __init__(self, address, port, timeout):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)
        self._sock.connect((address, port))
        self._file = self._sock.makefile('rwb', 0)

    def close(self):
        self._sock.close()

    def recv(self, n):
        return self._file.read(n)

    def recvline(self):
        return self._file.readline()[:-1]

    def recvlines(self, n):
        return [self.recvline() for i in range(n)]

    def send(self, data):
        return self._file.write(data)

    def sendline(self, data):
        return self.send(data + b'\n')
