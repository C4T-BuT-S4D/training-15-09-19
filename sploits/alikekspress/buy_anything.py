import sys

from ali_lib import *

PORT = 7000

mch = CheckMachine(sys.argv[1], PORT)

username, password = mch.register_user()
sess = mch.login_user(username, password)

if len(sys.argv) < 3:
    u, p = mch.register_user()
    sess_t = mch.login_user(u, p)
    item_id = mch.add_item(sess_t, 'test', 'flag_here', 1000000000)
else:
    item_id = sys.argv[2]

print(mch.buy_item(sess, item_id))
