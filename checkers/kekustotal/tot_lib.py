import base64
import requests
from checklib import *
from random import randint as R, choice
from elftools.elf.elffile import ELFFile
from binary_lib import generate_binary


PORT = 7001

class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/api'
    

    def __init__(self, host, port):
        self.host = host
        self.port = port


    def register_user(self):
        username = rnd_username()
        password = rnd_password()
        
        r = requests.post(f'{self.url}/register/', data={'username': username, 'password': password})
        check_response(r, 'Could not register')

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
        assert_eq('OK', get_json(r, 'Got invalid json response').get('result'), 'Could not register')

        return username, password


    def login_user(self, username, password):
        sess = get_initialized_session()
        
        r = sess.post(f'{self.url}/login/', data={'username': username, 'password': password})
        check_response(r, 'Could not login')
        
        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
        assert_eq('OK', get_json(r, 'Got invalid json response').get('result'), 'Could not login')

        return sess


    def invite(self, sess, userId, fileId):
        r = sess.post(f'{self.url}/invite/', data={'userId': userId, 'fileId': fileId})

        check_response(r, 'Could not invite user')

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
        assert_eq('OK', get_json(r, 'Got invalid json response').get('result'), 'Could not invite user')

        return get_json(r, 'Got invalid json response').get('result')


    def forbid(self, sess, userId, fileId):
        r = sess.post(f'{self.url}/forbid/', data={'userId': userId, 'fileId': fileId})

        check_response(r, 'Could not invite user')

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
        assert_eq('OK', get_json(r, 'Got invalid json response').get('result'), 'Could not forbid user')

        return get_json(r, 'Got invalid json response').get('result')


    def list(self, sess):
        r = sess.get(f'{self.url}/list/')

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')

        return get_json(r, 'Got invalid json response').get('result')


    def list_no_auth(self,):
        r = requests.get(f'{self.url}/list/')

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')

        return get_json(r, 'Got invalid json response').get('result')


    def download(self, sess, fileId, ok=True):
        r = sess.get(f'{self.url}/download/', params={'fileId': fileId})

        if ok:
            assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
            assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
        else:
            assert_in('error', get_json(r, 'Got invalid json response'), 'No error in response')
            assert_eq(False, get_json(r, 'Got invalid json response').get('ok'), 'Got true in ok response')

        return get_json(r, 'Got invalid json response').get('result')


    def info(self, sess, fileId):
        r = sess.get(f'{self.url}/info/', params={'fileId': fileId})

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')

        return get_json(r, 'Got invalid json response').get('result')


    def add_signature(self, sess, fileId, fileType, offsets, ok=True):
        offsets = ','.join(map(str, offsets))

        r = sess.post(f'{self.url}/signature/', data={
            'fileId': fileId,
            'fileType': fileType,
            'offsets': offsets
        })

        if ok:
            assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
            assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
            return get_json(r, 'Got invalid json response').get('result')
        else:
            assert_in('error', get_json(r, 'Got invalid json response'), 'No error in response')
            assert_eq(False, get_json(r, 'Got invalid json response').get('ok'), 'Got true in ok response')
            return None


    def get_signature(self, sess, fileId, offsets, ok=True):
        offsets = ','.join(map(str, offsets))

        r = sess.get(f'{self.url}/signature/', params={
            'fileId': fileId,
            'offsets': offsets
        })

        if ok:
            assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
            assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')
        else:
            assert_in('error', get_json(r, 'Got invalid json response'), 'No error in response')
            assert_eq(False, get_json(r, 'Got invalid json response').get('ok'), 'Got true in ok response')

        return get_json(r, 'Got invalid json response').get('result')


    def upload(self, sess, fileName):
        r = sess.post(f'{self.url}/upload/', files={'file': open(fileName, "rb")})

        assert_in('result', get_json(r, 'Got invalid json response'), 'No result in response')
        assert_eq(True, get_json(r, 'Got invalid json response').get('ok'), 'Got false in ok response')

        return get_json(r, 'Got invalid json response').get('result')


    def check_info(self, sess, fId, virus, notvirus, reviews):
        i = self.info(sess, fId)
        assert_in('virus', i, 'Incorrect info')
        assert_eq(i.get('virus'), virus, 'Incorrect info')
        assert_in('notVirus', i, 'Incorrect info')
        assert_eq(i.get('notVirus'), notvirus, 'Incorrect info')
        assert_in('reviews', i, 'Incorrect info')

        try:
            if sorted(i.get('reviews'), key=lambda k: (k['res'], k['sign'])) !=\
               sorted(reviews         , key=lambda k: (k['res'], k['sign'])):
                raise Exception("Invalid json on /info")
        except:
            cquit(Status.MUMBLE, "Invalid json on /info", "Invalid json on /info")


    def check_add_signature(self, sess, ssize, stext, fId, comment, ok=True):
        offsets = []

        while len(offsets) < 16:
            o = R(0, ssize - 1)
            if stext[o] == ord('.') or stext[o] == ord('/'):
                continue
            offsets.append(o)

        sign = self.add_signature(
            sess,
            fId,
            comment,
            offsets,
            ok
        )

        if sign is None:
            return None

        signOrigin = b""

        for off in offsets:
            c = stext[off]
            if 32 <= c < 127:
                signOrigin += chr(c).encode()
            else:
                signOrigin += b"\\x" + hex(c)[2:].zfill(2).encode()

        signOrigin = base64.b64encode(signOrigin).decode()

        assert_eq(sign, signOrigin, "Invalid signature")

        return sign


    def check_get_signature(self, sess, ssize, stext, fId, ok=True):
        offsets = []

        while len(offsets) < 16:
            o = R(0, ssize - 1)
            if stext[o] == ord('.') or stext[o] == ord('/'):
                continue
            offsets.append(o)

        sign = self.get_signature(
            sess,
            fId,
            offsets,
            ok
        )

        if sign is None:
            return None

        signOrigin = b""

        for off in offsets:
            c = stext[off]
            if 32 <= c < 127:
                signOrigin += chr(c).encode()
            else:
                signOrigin += b"\\x" + hex(c)[2:].zfill(2).encode()

        signOrigin = base64.b64encode(signOrigin).decode()

        assert_eq(sign, signOrigin, "Invalid signature")

        return sign


    def create_binary(self, text=None):
        b = generate_binary(text or rnd_string(10))

        with open(b, "rb") as f:
            elf = ELFFile(f)
            section = elf.get_section_by_name(".text")
            stext = section.data()
            ssize = section.data_size

        assert_neq(section, None, "No .text section")

        return b, ssize, stext