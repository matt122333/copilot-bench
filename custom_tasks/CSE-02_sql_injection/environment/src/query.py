import sqlite3
def get_user(db, name):
    cur = db.execute(f"SELECT * FROM users WHERE name = '{name}'")
    return cur.fetchall()
