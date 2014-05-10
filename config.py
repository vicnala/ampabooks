import web
import os.path
import sys

DATABASE = 'libros.sqlite'

def _touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()
        return True

    return False

def _init ():
    import sqlite3
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    from tables import items, item1, users, admin, grades, groups, tickets, students, books
    c.execute(items)
    c.execute(item1)
    c.execute(users)
    c.execute(admin)
    c.execute(grades)
    c.execute(groups)
    c.execute(tickets)
    c.execute(students)
    c.execute(books)
    conn.commit()
    conn.close()

if os.path.isfile(DATABASE):
    DB = web.database(dbn='sqlite', db=DATABASE)
else:
    print DATABASE, 'file not found'
    if _touch(DATABASE):
        print 'created', DATABASE
        _init()
        DB = web.database(dbn='sqlite', db=DATABASE)
    else:
        print 'Error crerating', DATABASE, 'file'
        sys.exit(1)


cache = False