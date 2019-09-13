#!/usr/bin/env python3

import os
import sys
import enum
import string
import requests
import secrets
import base64
import json
from hashlib import md5

from elftools.elf.elffile import ELFFile
from binary_lib import generate_binary
from random import randint as R

from checklib import *
from tot_lib import *


def put(host, flag_id, flag, vuln):
    mch = CheckMachine(host, PORT)
    
    u, p = mch.register_user()

    s = mch.login_user(u, p)

    b, ssize, stext = mch.create_binary(flag)

    fId = mch.upload(s, b)

    fType = rnd_string(7)

    sign = mch.check_add_signature(s, ssize, stext, fId, fType)

    cquit(Status.OK, json.dumps({
        "u": u,
        "p": p,
        "fId": fId,
        "fType": fType,
        "sign": sign,
    }))


def get(host, flag_id, flag, vuln):
    mch = CheckMachine(host, PORT)
    
    d = json.loads(flag_id)

    u, p, fId, fType, sign = d["u"], d["p"], d["fId"], d["fType"], d["sign"]

    s = mch.login_user(u, p)

    f = mch.download(s, fId)

    assert_in(flag.encode(), base64.b64decode(f.encode()), "No flag in file", Status.CORRUPT)

    mch.check_info(s, fId, 0, 1, [
        {'res': fType, 'sign': sign}
    ])

    mch.check_get_signature(s, ssize, stext, fId)

    u2, p2 = mch.register_user()

    s2 = mch.login_user(u2, p2)

    mch.check_get_signature(s2, ssize, stext, fId)

    mch.check_add_signature(
        s2,
        ssize,
        stext,
        fId,
        fType,
        choice(["malware", "worm", "trojan", "virus"])
    )

    assert_in('session', s2.cookies, 'Invalid session')

    uid3 = s2.cookies['session']

    mch.invite(s, uid, fId)

    sign = mch.check_add_signature(
        s2,
        ssize,
        stext,
        fId,
        choice(["malware", "worm", "trojan", "virus"])
    )

    mch.check_info(s2, fId, 1, 0, [
        {'res': 'virus', 'sign': sign}
    ])

    l = mch.list_no_auth()

    assert_in(fId, l, 'Could not find flag file')

    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host, PORT)
    
    u1, p1 = mch.register_user()

    s1 = mch.login_user(u1, p1)

    b1, ssize1, sectionText1 = mch.create_binary()

    fId1 = mch.upload(s1, b1)

    fDownload1 = mch.download(s1, fId1)

    with open(b1, "rb") as f:
        fOrigin1 = f.read()

    assert_eq(
        md5(fDownload1.encode()).hexdigest(),
        md5(base64.b64encode(fOrigin1)).hexdigest(),
        "Incorrect file"
    )

    mch.check_info(s1, fId1, 0, 0, [])

    sign1virus = mch.check_add_signature(
        s1,
        ssize1,
        sectionText1,
        fId1,
        choice(["malware", "worm", "trojan", "virus"])
    )

    mch.check_info(s1, fId1, 1, 0, [
        {'res': 'virus', 'sign': sign1virus}
    ])

    fType = rnd_string(7)

    sign1notvirus = mch.check_add_signature(
        s1,
        ssize1,
        sectionText1,
        fId1,
        fType
    )

    mch.check_info(s1, fId1, 1, 1, [
        {'res': 'virus', 'sign': sign1virus},
        {'res': fType, 'sign': sign1notvirus}
    ])

    mch.check_get_signature(
        s1,
        ssize1,
        sectionText1,
        fId1
    )

    l = mch.list_no_auth()

    assert_in(fId1, l, 'Could not find file')

    u2, p2 = mch.register_user()

    s2 = mch.login_user(u2, p2)

    b2, ssize2, sectionText2 = mch.create_binary()

    fId2 = mch.upload(s2, b2)

    l = mch.list_no_auth()

    assert_in(fId2, l, 'Could not find file')

    u3, p3 = mch.register_user()

    s3 = mch.login_user(u3, p3)

    mch.download(s3, fId2, False)

    mch.check_add_signature(
        s3,
        ssize2,
        sectionText2,
        fId2,
        choice(["malware", "worm", "trojan", "virus"]),
        False
    )

    fType = rnd_string(7)

    mch.check_add_signature(
        s3,
        ssize2,
        sectionText2,
        fId2,
        fType,
        False
    )

    assert_in('session', s3.cookies, 'Invalid session')

    uid3 = s3.cookies['session']

    mch.check_info(s3, fId2, 0, 0, [])

    mch.invite(s2, uid3, fId2)

    mch.download(s3, fId2)

    sign = mch.check_add_signature(
        s3,
        ssize2,
        sectionText2,
        fId2,
        choice(["malware", "worm", "trojan", "virus"])
    )

    mch.check_info(s3, fId2, 1, 0, [
        {'res': 'virus', 'sign': sign}
    ])

    l = mch.list_no_auth()

    u4, p4 = mch.register_user()

    s4 = mch.login_user(u4, p4)

    mch.check_get_signature(
        s4,
        ssize1,
        sectionText1,
        fId1
    )

    assert_in(fId2, l, 'Could not find file')

    cquit(Status.OK)


if __name__ == '__main__':
    action, *args = sys.argv[1:]
    try:
        if action == "check":
            host, = args
            check(host)
        elif action == "put":
            host, flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)
        elif action == "get":
            host, flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)
        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))
