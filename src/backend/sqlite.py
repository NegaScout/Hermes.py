from os.path import isfile
from sqlite3 import connect

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(SQL_PATH)

def commit():
    db_conn.commit()

def close():
    db_conn.close()

def scriptexec(cursor, path):
    with open(path, 'r', encoding="utf-8") as script:
        cursor.executescript(script.read())