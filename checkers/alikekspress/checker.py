#!/usr/bin/env python3

import os
import sys
import enum
import string
import requests
import secrets
import random

from checklib import *
from ali_lib import *


def put(host, flag_id, flag, vuln):
    mch = CheckMachine(host, PORT)
    username, password = mch.register_user()
    sess = mch.login_user(username, password)

    name = rnd_string(20)
    description = rnd_string(random.randint(100, 200)) + flag + rnd_string(random.randint(100, 200))
    cost = random.randint(10 ** 9, 2 * 10 ** 9)
    item_id = mch.add_item(sess, name, description, cost)

    cquit(Status.OK, f'{item_id}:{username}:{password}:{cost}')


def get(host, flag_id, flag, vuln):
    mch = CheckMachine(host, PORT)
    item_id, username, password, cost = flag_id.split(':')
    sess = mch.login_user(username, password)
    item = mch.get_item(sess, item_id)
    assert_in(flag, item.get('description'), 'Could not get flag for item', status=Status.CORRUPT)
    assert_eq(cost, cost, 'Invalid item data')

    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host, PORT)
    username, password = mch.register_user()
    sess = mch.login_user(username, password)
    data = mch.get_me(sess)
    assert_eq(username, data.get('username'), 'Invalid user data')
    assert_eq(10, data.get('money'), 'Invalid user data')

    username, password = mch.change_user(sess, 5)
    sess = mch.login_user(username, password)
    data = mch.get_me(sess)
    assert_eq(username, data['username'], 'Invalid user data')
    assert_eq(5, data.get('money'), 'Invalid user data')

    item_name = rnd_string(20)
    item_description = rnd_string(100)
    cost = random.randint(1, 5)
    item_id = mch.add_item(sess, item_name, item_description, cost)
    my_items = mch.get_my_items(sess)
    assert_in_list_dicts(my_items, 'id', item_id, 'Could not find added item')

    item = mch.get_item(sess, item_id)
    assert_eq(cost, item.get('cost'), 'Invalid item data')
    assert_eq(item_name, item.get('name'), 'Invalid item data')
    assert_eq(item_description, item.get('description'), 'Invalid item data')

    cost = random.randint(10, 100)
    mch.change_item(sess, cost, item_id)
    item = mch.get_item(sess, item_id)
    assert_eq(cost, item.get('cost'), 'Invalid item data')

    item = mch.get_item(requests, item_id)
    assert_eq(cost, item.get('cost'), 'Invalid item data')

    all_items = mch.get_all_items(requests)
    assert_in_list_dicts(all_items, 'id', item_id, 'Could not find added item')

    fake_username, fake_password = mch.register_user()
    fake_sess = mch.login_user(fake_username, fake_password)

    mch.change_item(sess, 10, item_id)
    mch.buy_item(fake_sess, item_id)
    new_user = mch.get_me(sess)
    assert_gt(19, new_user['money'], 'Invalid user data')

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
