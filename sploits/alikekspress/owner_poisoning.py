import sys

from ali_lib import *

PORT = 7000

mch = CheckMachine(sys.argv[1], PORT)

username, password = mch.register_user()
sess = mch.login_user(username, password)

item_id = sys.argv[2]

user_id = mch.get_me(sess)['id']
mch.change_item(sess, 10, item_id)
print(mch.get_item(sess, item_id))
