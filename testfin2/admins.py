import sqlite3
import testfin2

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('admins.db')
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
    c.execute('INSERT INTO user_message (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()


def del_message(user_id: int, username: str):
    conn = get_connection()
    c = conn.cursor()
    d = "DELETE FROM user_message WHERE username = {}".format("'" + username + "'")
    c.execute(d)
    conn.commit()



def get_info():
    conn = get_connection()
    c = conn.cursor()
    return c.execute("SELECT user_id, username FROM user_message ORDER BY id")


if __name__ == '__main__':
    init_db()

    # add_message('379618549', 'kirr_ya')

    get_info()
