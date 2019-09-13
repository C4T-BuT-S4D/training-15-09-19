from subprocess import Popen
from random import randint as R, choice
from checklib import *

prints = [
"""
printf("{}");
""",

"""
puts("{}");
""",

"""
printf("%s", "{}");
""",

"""
write(1, "{}", {});
"""
]

template = """
#include <stdio.h>
#include <unistd.h>

int main() {{
    {}
}}
"""

def generate_binary(text):
    name = rnd_string(15)

    with open(f"/tmp/{name}.c", "w") as f:
        code = ""

        l = R(3, 6)
        r = R(3, 6)

        for i in range(l):
            code += choice(prints).format(rnd_string(10), 10)

        code += choice(prints).format(text, len(text))

        for i in range(r):
            code += choice(prints).format(rnd_string(10), 10)

        f.write(template.format(code))

    p = Popen(["gcc", f"/tmp/{name}.c", "-o", f"/tmp/{name}"])
    p.wait()

    return f"/tmp/{name}"