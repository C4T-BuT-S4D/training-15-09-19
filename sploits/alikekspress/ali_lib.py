import base64

import requests
from checklib import *

PORT = 7000


def make_request(module, method, url, **kwargs):
    method = base64.b32encode(method.encode()).decode().strip('=')
    return module.request(method, url=url, **kwargs)


class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def register_user(self):
        username = rnd_username()
        password = rnd_password()

        r = make_request(requests, 'reg_post', f'{self.url}/register/',
                         data={'username': username, 'password': password})
        check_response(r, 'Could not register')
        return username, password

    def login_user(self, username, password):
        sess = get_initialized_session()

        r = make_request(sess, 'log_post', f'{self.url}/login/', data={'username': username, 'password': password})
        check_response(r, 'Could not login')

        return sess

    def change_user(self, sess, money):
        new_username = rnd_username()
        new_password = rnd_password()
        r = make_request(
            sess, 'edu_post', f'{self.url}/edit_user/',
            data={'username': new_username, 'password': new_password, 'money': money},
        )
        check_response(r, 'Could not change user')

        return new_username, new_password

    def get_me(self, sess):
        r = make_request(sess, 'user_get', f'{self.url}/me/')
        return get_json(r, 'Could not get me')

    def add_item(self, sess, name, description, cost):
        cost = cost

        r = make_request(
            sess, 'item_post', f'{self.url}/add_item/',
            data={'name': name, 'description': description, 'cost': cost},
        )
        check_response(r, 'Could not add item')

        return int(r.text)

    def change_item(self, sess, cost, item_id):
        name = rnd_string(20)
        description = rnd_string(200)
        cost = cost

        r = make_request(
            sess, 'item_put', f'{self.url}/change_item/{item_id}/',
            data={'name': name, 'description': description, 'cost': cost},
        )
        check_response(r, 'Could not change item')

    def get_my_items(self, sess):
        r = make_request(sess, 'u_item_list', f'{self.url}/items/my/')
        check_response(r, 'Could not get user items')
        return get_json(r, 'Could not get user items')

    def get_all_items(self, sess):
        r = make_request(sess, 'a_item_list', f'{self.url}/items/all/')
        check_response(r, 'Could not get all items')
        return get_json(r, 'Could not get all items')

    def get_item(self, sess, item_id):
        r = make_request(sess, 'item_retrieve', f'{self.url}/items/get/{item_id}/')
        check_response(r, 'Could not fetch item')
        return get_json(r, 'Could not fetch item')

    def buy_item(self, sess, item_id):
        r = make_request(sess, 'buy_item', f'{self.url}/buy/{item_id}/')
        check_response(r, 'Could not buy item')
        return get_json(r, 'Could not buy item')
