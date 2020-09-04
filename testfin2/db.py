import sqlite3
import testfin2

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('users.db')
    return __connection


def init_db(force=False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
        id          INTEGER PRIMARY KEY,
        user_id     INTEGER NOT NULL,
        username    TEXT NOT NULL
        )      
    ''')

    conn.commit()


def add_message(user_id: int, username: str):
    conn = get_connection()
    c = conn.cursor()
    if bool(username):
        c.execute('INSERT INTO user_message (user_id, username) VALUES (?, ?)', (user_id, username))
    else:
        c.execute('INSERT INTO user_message (user_id, username) VALUES (?, ?)', (user_id, 'null'))
    conn.commit()


# def list_info(user_id: int, username: str):
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('SELECT user_id, username from user_message', (user_id, username))
#     return c.fetchall()


def get_info():
    conn = get_connection()
    c = conn.cursor()
    return c.execute("SELECT user_id, username FROM user_message ORDER BY id")


if __name__ == '__main__':
    init_db()
    # init_db(True)

    add_message('292668410', 'TimurUt')
    add_message('697896713', 'null')
    add_message('595359025', 'Danila_Yudin')
    get_info()
