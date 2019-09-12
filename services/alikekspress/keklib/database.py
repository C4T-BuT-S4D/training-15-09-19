import MySQLdb
from contextlib import contextmanager

conn = MySQLdb.connect(
    host="mysql",
    user="alikexpress",
    passwd="secretpass",
    db="alikexpress",
)


@contextmanager
def database(dict_cursor=False):
    if dict_cursor:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    else:
        curs = conn.cursor()
    try:
        yield curs, conn
    finally:
        curs.close()
