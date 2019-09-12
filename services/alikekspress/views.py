from app import app
from keklib import decorators, security
from keklib.database import database
from flask import request, session, abort, jsonify


@app.endpoint('register')
@decorators.with_allowed_methods(['reg_post'])
def register():
    data = request.form.to_dict()

    if not data.get('username') or not data.get('password'):
        return 'Specify username, password', 400

    with database() as (curs, conn):
        query = "SELECT id FROM users WHERE username=%s"
        curs.execute(query, (data['username'],))
        user = curs.fetchone()
        if user is not None:
            return 'Already registered', 400

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        curs.execute(query, (data['username'], data['password']))
        conn.commit()

    return 'OK', 201


@app.endpoint('login')
@decorators.with_allowed_methods(['log_post'])
def login():
    data = request.form.to_dict()

    if not data.get('username') or not data.get('password'):
        return 'Specify username, password', 400

    with database(True) as (curs, _):
        query = "SELECT id FROM users WHERE username=%s AND password=%s"
        curs.execute(query, (data['username'], data['password']))
        user = curs.fetchone()
        if user is None:
            return 'No such user', 400
        session['id'] = user['id']

    return 'OK'


@app.endpoint('edit_user')
@decorators.with_allowed_methods(['edu_post'])
@decorators.login_required
def edit_user():
    data = request.form.to_dict()

    if data.get('money'):
        with database(True) as (curs, conn):
            query = 'SELECT money FROM users WHERE id=%s'
            curs.execute(query, (session['id'],))
            user = curs.fetchone()

        if user['money'] < int(data['money']):
            data['money'] = user['money']

    keys = list(map(
        lambda x: security.quote_identifier(x).replace('"', '`'),
        data.keys(),
    ))
    values = list(map(security.quote_identifier, data.values()))
    query = ', '.join(map(lambda x: f'{x[0]}={x[1]}', zip(keys, values)))

    with database(True) as (curs, conn):
        query = "UPDATE users SET " + query + " WHERE id=" + str(session['id'])
        curs.execute(query)
        conn.commit()

    return 'OK'


@app.endpoint('get_user')
@decorators.with_allowed_methods(['user_get'])
@decorators.login_required
def edit_user():
    with database(True) as (curs, _):
        query = 'SELECT id, username, money FROM users WHERE id=%s'
        curs.execute(query, (session['id'],))
        user = curs.fetchone()

    return jsonify(dict(user))


@app.endpoint('add_item')
@decorators.login_required
@decorators.with_allowed_methods(['item_post'])
def create_item():
    data = request.form.to_dict()

    data['owner_id'] = data.get('owner_id') or session['id']
    key_part = ', '.join(map(
        lambda x: security.quote_identifier(x).replace('"', ''),
        data.keys()),
    )
    value_path = ', '.join(['%s'] * len(list(data.values())))

    query = f'INSERT INTO items ({key_part}) VALUES ({value_path})'
    args = list(data.values())
    with database() as (curs, conn):
        curs.execute(query, args)
        conn.commit()

        query = "SELECT LAST_INSERT_ID()"
        curs.execute(query)
        result, = curs.fetchone()

    return str(result), 201


@app.endpoint('change_item')
@decorators.with_allowed_methods(['item_put'])
@decorators.login_required
def change_item(item_id):
    data = request.form.to_dict()

    data['owner_id'] = data.get('owner_id') or session['id']
    keys = list(map(
        lambda x: security.quote_identifier(x).replace('"', '`'),
        data.keys(),
    ))
    values = list(map(security.quote_identifier, map(str, data.values())))
    query = ', '.join(map(lambda x: f'{x[0]}={x[1]}', zip(keys, values)))

    query = f'UPDATE items SET {query} WHERE id=%s'
    print(query)
    with database() as (curs, conn):
        curs.execute(query, (item_id,))
        conn.commit()

    return 'OK'


@app.endpoint('list_my_items')
@decorators.login_required
@decorators.with_allowed_methods(['u_item_list'])
def list_my_items():
    offset = request.args.get('offset', 0)
    with database(True) as (curs, _):
        query = """
        SELECT id, name, description, cost, owner_id 
        FROM items 
        WHERE owner_id=%s 
        ORDER BY id DESC LIMIT %s, 1000
        """
        curs.execute(query, (session['id'], offset))
        items = curs.fetchall()

    return jsonify(list(map(dict, items)))


@app.endpoint('list_all_items')
@decorators.with_allowed_methods(['a_item_list'])
def list_all_items():
    offset = request.args.get('offset', 0)
    with database(True) as (curs, _):
        query = 'SELECT id, name, cost, owner_id FROM items ORDER BY id DESC LIMIT %s, 1000'
        curs.execute(query, (offset,))
        items = curs.fetchall()

    return jsonify(list(map(dict, items)))


@app.endpoint('get_item')
@decorators.with_allowed_methods(['item_retrieve'])
def get_item(item_id):
    with database(True) as (curs, _):
        query = 'SELECT id, name, description, cost, owner_id FROM items WHERE id=%s'
        curs.execute(query, (item_id,))
        item = curs.fetchone()

    if item is None:
        abort(404)

    item = dict(item)
    if item['owner_id'] != session.get('id'):
        item.pop('description')

    return jsonify(item)


@app.endpoint('buy_item')
@decorators.login_required
@decorators.with_allowed_methods(['buy_item'])
def buy_item(item_id):
    with database(True) as (curs, _):
        query = "SELECT * FROM items WHERE id=%s"
        curs.execute(query, (item_id,))
        item = curs.fetchone()

    if item is None:
        abort(404)

    with database(True) as (curs, conn):
        query = "SELECT money FROM users WHERE id=%s"
        curs.execute(query, (session['id'],))
        prev_money, = curs.fetchone()

        query = "UPDATE users SET money = money - (SELECT cost FROM items WHERE id=%s) WHERE id=%s"
        curs.execute(query, (item_id, session['id']))
        conn.commit()

        query = "UPDATE users SET money = money + (SELECT cost FROM items WHERE id=%s) WHERE id=%s"
        curs.execute(query, (item_id, item['owner_id']))
        conn.commit()

        query = "SELECT money FROM users WHERE id=%s"
        curs.execute(query, (session['id'],))
        new_money = curs.fetchone()['money']

        if new_money < 0:
            query = "UPDATE users SET money = %s WHERE id=%s"
            curs.execute(query, (prev_money, session['id']))
            conn.commit()
            return 'Not enough money', 403

    return jsonify(dict(item))
