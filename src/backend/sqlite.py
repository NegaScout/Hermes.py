from os.path import isfile
from sqlite3 import connect


def self_with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        args[0].db_conn.commit()

    return inner


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        args[0].db_conn.commit()

    return inner


# @with_commit
# def commit(db_conn):
#    db_conn.commit()


def close(db_conn):
    db_conn.close()


def scriptexec(cursor, path):
    try:
        with open(path, "r", encoding="utf-8") as script:
            cursor.executescript(script.read())
    except OSError as e:
        print(e)
