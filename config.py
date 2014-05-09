import web
import os.path
import sys


def _touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()
        return True

    return False

if os.path.isfile('libros.sqlite'):
    DB = web.database(dbn='sqlite', db='libros.sqlite')
else:
    print 'libros.sqlite file not found'
    if _touch('libros.sqlite'):
        print 'created libros.sqlite file'
        import sqlite3
        conn = sqlite3.connect('libros.sqlite')
        c = conn.cursor()
        from tables import items, item1
        c.execute(items)
        c.execute(item1)
        conn.commit()
        conn.close()

        DB = web.database(dbn='sqlite', db='libros.sqlite')
    else:
        print 'ERROR crerating libros.sqlite'
        sys.exit(1)


cache = False