import web
import os.path
import sys
import shutil

DATABASE = 'db/libros.sqlite'

def _touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()
        return True

    return False

def _init():
    import sqlite3
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    from tables import items, item1, users, admin, org, nif, grades, groups, tickets, students, books, default_grade, default_group
    c.execute(items)
    c.execute(item1)
    c.execute(users)
    c.execute(admin)
    c.execute(org)
    c.execute(nif)
    c.execute(grades)
    c.execute(default_grade)
    c.execute(groups)
    c.execute(default_group)
    c.execute(tickets)
    c.execute(students)
    c.execute(books)
    conn.commit()
    conn.close()

def _copy_blank():
    shutil.copy2(DATABASE, 'db/libros-vacia.sqlite')

if os.path.isfile(DATABASE):
    DB = web.database(dbn='sqlite', db=DATABASE)
else:
    print DATABASE, 'file not found.'
    if _touch(DATABASE):
        print 'initializing database', DATABASE, '...'
        _init()
        _copy_blank()
        DB = web.database(dbn='sqlite', db=DATABASE)
    else:
        print 'Error crerating', DATABASE, 'file.'
        sys.exit(1)


cache = False