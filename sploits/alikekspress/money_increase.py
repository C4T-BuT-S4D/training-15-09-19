import sys

from ali_lib import *

PORT = 7000

mch = CheckMachine(sys.argv[1], PORT)

username, password = mch.register_user()
sess = mch.login_user(username, password)

item_id = mch.add_item(sess, 'test', 'test', 100000000)
print('Was:', mch.get_me(sess))
mch.buy_item(sess, item_id)
print('Now:', mch.get_me(sess))
