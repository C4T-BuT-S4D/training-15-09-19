from flask import Flask
from werkzeug.routing import Rule

app = Flask(__name__)
app.secret_key = 'change_me'

from keklib.error_handlers import *
from views import *

app.url_map.add(Rule('/register/', endpoint='register'))
app.url_map.add(Rule('/login/', endpoint='login'))
app.url_map.add(Rule('/edit_user/', endpoint='edit_user'))
app.url_map.add(Rule('/me/', endpoint='get_user'))
app.url_map.add(Rule('/add_item/', endpoint='add_item'))
app.url_map.add(Rule('/change_item/<item_id>/', endpoint='change_item'))
app.url_map.add(Rule('/items/my/', endpoint='list_my_items'))
app.url_map.add(Rule('/items/all/', endpoint='list_all_items'))
app.url_map.add(Rule('/items/get/<item_id>/', endpoint='get_item'))
app.url_map.add(Rule('/buy/<item_id>/', endpoint='buy_item'))


@app.before_first_request
def init_db():
    with database() as (curs, conn):
        query = "SET sql_mode = 'NO_UNSIGNED_SUBTRACTION'"
        curs.execute(query)

        query = """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                username varchar(255),
                password varchar(255),
                money INT UNSIGNED DEFAULT 10
        )"""
        curs.execute(query)

        query = """
            CREATE TABLE IF NOT EXISTS items(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name varchar(255),
                description TEXT,
                cost INT UNSIGNED,
                owner_id INTEGER
        )"""
        curs.execute(query)

        conn.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
