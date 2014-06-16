import web
import config
from datetime import datetime
from forms import useradd_form, gradeadd_form, groupadd_form, studadd_form, bookadd_form
import csv
import sqlite3
import os
import shutil
from render import render

grades = []
groups = []

def admin_get():
    return render.admin()



def grades_get():
    grades = config.DB.select('grades')
    return render.grades(grades)

def grades_post():
    i = web.input()
    for grades_id in i:
        config.DB.delete('grades', where="id=$grades_id", vars=locals())
    raise web.seeother('/admin/grades')

def gradeadd_get():
    return render.gradeadd(gradeadd_form)

def gradeadd_post():
    if not gradeadd_form.validates(): 
        return render.gradeadd(gradeadd_form)
    else:
        try:
            config.DB.insert('grades', grade=gradeadd_form.d.curso)
        except:
            return "El curso ya existe!"
        raise web.seeother('/admin/grades')



def groups_get():
    groups = config.DB.select('groups')
    return render.groups(groups)

def groups_post():
    i = web.input()
    for groups_id in i:
        config.DB.delete('groups', where="id=$groups_id", vars=locals())
    raise web.seeother('/admin/groups')

def groupadd_get():
    return render.groupadd(groupadd_form)

def groupadd_post():
    if not groupadd_form.validates(): 
        return render.groupadd(groupadd_form)
    else:
        try:
            print groupadd_form.d.grupo
            config.DB.insert('groups', groupe=groupadd_form.d.grupo)
        except:
            return "El grupo ya existe!"
        raise web.seeother('/admin/groups')




def users_get():
    users = config.DB.select('users')
    return render.users(users)

def users_post():
    i = web.input()
    for key, value in i.items():
        if value in 'on':
            raise web.seeother('/useredit/' + key)



def useradd_get():
    return render.useradd(useradd_form)

def useradd_post():
    if not useradd_form.validates(): 
        return render.login(useradd_form)
    else:
        try:
            config.DB.insert('users', username=useradd_form.d.username, name=useradd_form.d.name)
        except:
            return "El usuario ya existe, elige otro."
        raise web.seeother('/admin/users')


def useredit_get(_id):
    user = config.DB.select('users', where="id=$_id limit 1", vars=locals())
    if user is not None:
        return render.useredit(user)
    else:
        raise web.seeother('/admin/users')


def useredit_post(_id):
    i = web.input()
    user_data = config.DB.select('users', where="id=$_id limit 1", vars=locals())
    data = {}
    if user_data is not None:
        for k, v in user_data[0].items():
            data[k] = v

    delete = False
    print data

    for key, value in i.items():
        if key in "nick_" + str(_id):
            data['username'] = value
        elif key in "name_" + str(_id):
            data['name'] = value
        elif key in "delete_" + str(_id):
            delete = True

    print data

    if delete:
        config.DB.delete('users', where="id=$_id", vars=locals())
    else:
        config.DB.update('users', where="id=$_id", username=data['username'], name=data['name'], vars=locals())

    raise web.seeother('/admin/users')






def students_get():
    students = config.DB.select('students')
    return render.students(students, {})

def students_post():
    i = web.input()
    for key, value in i.items():
        if value in 'on':
            raise web.seeother('/studedit/' + key)


def studadd_get():
    del grades[:]
    db_grades = config.DB.select('grades')
    for grade in db_grades:
        grades.append((grade.grade, grade.grade))

    del groups[:]
    db_groups = config.DB.select('groups')
    for group in db_groups:
        groups.append((group.groupe, group.groupe))
    f = studadd_form(grades, groups)
    return render.studadd(f)

def studadd_post():
    f = studadd_form(grades, groups)
    if not f.validates(): 
        return render.studadd(f)
    else:
        config.DB.insert('students', nombre=f.d.nombre, curso=f.d.curso, grupo=f.d.grupo, tutor=f.d.tutor, tel1=f.d.tel1, tel2=f.d.tel2, mail1=f.d.mail1, mail2=f.d.mail2)
        raise web.seeother('/admin/students')



def studedit_get(_id):
    stud = config.DB.select('students', where="id=$_id", vars=locals())
    if stud is not None:
        db_grades = config.DB.select('grades')
        db_groups = config.DB.select('groups')

        return render.studedit(stud, db_grades, db_groups)
    else:
        raise web.seeother('/admin/students')


def studedit_post(_id):
    i = web.input()
    delete = False

    stud_data = config.DB.select('students', where="id=$_id", vars=locals())
    data = {}

    if stud_data is not None:
        for k, v in stud_data[0].items():
            data[k] = v

    for key, value in i.items():
        #print key, value
        if key in "nombre_" + str(_id):
            data['nombre'] = value
        elif key in "curso_" + str(_id):
            data['curso'] = value
        elif key in "grupo_" + str(_id):
            data['grupo'] = value
        elif key in "tutor_" + str(_id):
            data['tutor'] = value
        elif key in "tel1_" + str(_id):
            data['tel1'] = value
        elif key in "tel2_" + str(_id):
            data['tel2'] = value
        elif key in "mail1_" + str(_id):
            data['mail1'] = value
        elif key in "mail2_" + str(_id):
            data['mail2'] = value
        elif key in "delete_" + str(_id):
            delete = True

    if delete:
        config.DB.delete('students', where="id=$_id", vars=locals())
    else:
        config.DB.update('students', where="id=$_id", nombre=data['nombre'], curso=data['curso'], 
            tutor=data['tutor'], tel1=data['tel1'], tel2=data['tel2'], mail1=data['mail1'],
            mail2=data['mail2'], grupo=data['grupo'], vars=locals())

    raise web.seeother('/admin/students')


def studexport_get():
    students = config.DB.select('students')
    data = []
    data.append('nombre,curso,grupo,tutor,tel1,tel2,mail1,mail2')
    for stud in students:
        row = []
        row.append(stud['nombre'])
        row.append(stud['curso'])
        row.append(stud['grupo'])
        row.append(stud['tutor'])
        row.append(stud['tel1'])
        row.append(stud['tel2'])
        row.append(stud['mail1'])
        row.append(stud['mail2'])
        data.append(",".join(row))

    web.header('Content-Type','text/csv')
    web.header('Content-disposition', 'attachment; filename=alumnos.csv')
    return "\n".join(data)


def studimport_get():
    return render.studimport()


def studimport_post():
    x = web.input(myfile={})
    if 'myfile' in x:
        fname = 'tmp/alumnos.csv'
        f = open(fname, 'w')
        f.write(x.myfile.file.read())
        f.close()

        grades_db = config.DB.select('grades')
        groups_db = config.DB.select('groups')

        grades_db_list = []
        groups_db_list = []

        new_grades = []
        new_groups = []

        with open(fname, 'rb') as data:
            try:
                # csv.DictReader uses first line in file for column headings by default
                dr = csv.DictReader(data) # comma is default delimiter
                to_db = [(i['nombre'], i['curso'], i['grupo'].upper(), i['tutor'], i['tel1'],
                         i['tel2'], i['mail1'], i['mail2']) for i in dr]
                for gdb in grades_db:
                    grades_db_list.append(gdb['grade'])

                for gdb in groups_db:
                    groups_db_list.append(gdb['groupe'])

                for item in to_db:
                    if item[1] in grades_db_list:
                        pass
                    else:
                        new_grades.append(item[1])
                        grades_db_list.append(item[1])
                    if item[2] in groups_db_list:
                        pass
                    else:
                        new_groups.append(item[2])
                        groups_db_list.append(item[2])
                        
                print new_grades, new_groups
                os.remove(fname)
            except Exception, e:
                os.remove(fname)
                return render.error('csv.DictReader', e)
            else:
                con = sqlite3.connect('db/libros.sqlite')
                con.text_factory = str
                cur = con.cursor()
                try:
                    cur.executemany('''INSERT INTO students (nombre, curso, grupo, tutor, 
                                        tel1, tel2, mail1, mail2)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                                        to_db)
                    con.commit()
                except Exception, e:
                    return render.error('SQLite', e)

                for grade in new_grades:
                    config.DB.insert('grades', grade=grade)

                for group in new_groups:
                    config.DB.insert('groups', groupe=group)

    raise web.seeother('/admin/students')




def books_get():
    books = config.DB.select('books')
    return render.books(books, {})

def books_post():
    i = web.input()
    for key, value in i.items():
        if value in 'on':
            raise web.seeother('/bookedit/' + key)


def bookadd_get():
    grades = []
    db_grades = config.DB.select('grades')
    for grade in db_grades:
        grades.append((grade.grade, grade.grade))

    groups = []
    db_groups = config.DB.select('groups')
    for group in db_groups:
        groups.append((group.groupe, group.groupe))
    f = bookadd_form(grades, groups)
    return render.bookadd(f)

def bookadd_post():
    f = bookadd_form(grades, groups)
    if not f.validates(): 
        return render.bookadd(f)
    else:
        config.DB.insert('books', titulo=f.d.titulo, curso=f.d.curso, grupo=f.d.grupo, editorial=f.d.editorial, isbn=f.d.isbn, precio=f.d.precio, stock=f.d.stock)
        raise web.seeother('/admin/books')



def bookedit_get(_id):
    book = config.DB.select('books', where="id=$_id", vars=locals())
    if book is not None:
        db_grades = config.DB.select('grades')
        db_groups = config.DB.select('groups')

        return render.bookedit(book, db_grades, db_groups)
    else:
        raise web.seeother('/admin/books')


def bookedit_post(_id):
    i = web.input()
    delete = False

    book_data = config.DB.select('books', where="id=$_id", vars=locals())
    data = {}

    if book_data is not None:
        for k, v in book_data[0].items():
            data[k] = v

    for key, value in i.items():
        #print key, value
        if key in "titulo_" + str(_id):
            data['titulo'] = value
        elif key in "curso_" + str(_id):
            data['curso'] = value
        elif key in "grupo_" + str(_id):
            data['grupo'] = value
        elif key in "editorial_" + str(_id):
            data['editorial'] = value
        elif key in "isbn_" + str(_id):
            data['isbn'] = value
        elif key in "precio_" + str(_id):
            data['precio'] = value
        elif key in "stock_" + str(_id):
            data['stock'] = value
        elif key in "delete_" + str(_id):
            delete = True

    if delete:
        config.DB.delete('books', where="id=$_id", vars=locals())
    else:
        config.DB.update('books', where="id=$_id", titulo=data['titulo'], curso=data['curso'], 
            editorial=data['editorial'], isbn=data['isbn'], precio=data['precio'], 
            stock=int(data['stock']), grupo=data['grupo'], vars=locals())

    raise web.seeother('/admin/books')


def bookexport_get():
    books = config.DB.select('books')
    data = []
    data.append('titulo,curso,grupo,editorial,isbn,precio,stock')
    for book in books:
        row = []
        row.append(book['titulo'])
        row.append(book['curso'])
        row.append(book['grupo'])
        row.append(book['editorial'])
        row.append(book['isbn'])
        row.append(book['precio'])
        row.append(str(book['stock']))
        data.append(",".join(row))

    web.header('Content-Type','text/csv')
    web.header('Content-disposition', 'attachment; filename=libros.csv')
    return "\n".join(data)



def bookimport_get():
    return render.bookimport()

def bookimport_post():
    x = web.input(myfile={})
    if 'myfile' in x:
        fname = 'tmp/libros.csv'
        f = open(fname, 'w')
        f.write(x.myfile.file.read())
        f.close()

        grades_db = config.DB.select('grades')
        groups_db = config.DB.select('groups')

        grades_db_list = []
        groups_db_list = []

        new_grades = []
        new_groups = []

        with open(fname, 'rb') as data:
            try:
                # csv.DictReader uses first line in file for column headings by default
                dr = csv.DictReader(data) # comma is default delimiter
                to_db = [(i['titulo'], i['curso'], i['grupo'].upper(), i['editorial'], i['isbn'],
                         i['precio'], i['stock']) for i in dr]

                for gdb in grades_db:
                    grades_db_list.append(gdb['grade'])

                for gdb in groups_db:
                    groups_db_list.append(gdb['groupe'])

                for item in to_db:
                    if item[1] in grades_db_list:
                        pass
                    else:
                        new_grades.append(item[1])
                        grades_db_list.append(item[1])
                    if item[2] in groups_db_list:
                        pass
                    else:
                        new_groups.append(item[2])
                        groups_db_list.append(item[2])
                        
                print new_grades, new_groups

                os.remove(fname)
            except Exception, e:
                os.remove(fname)
                return render.error('csv.DictReader', e)
            else:
                con = sqlite3.connect('db/libros.sqlite')
                con.text_factory = str
                cur = con.cursor()
                try:
                    print to_db
                    cur.executemany('''INSERT INTO books (titulo, curso, grupo, editorial, 
                                        isbn, precio, stock)
                                        VALUES (?, ?, ?, ?, ?, ?, ?);''',
                                        to_db)

                    con.commit()

                except Exception, e:
                    return render.error('SQLite', e)

                for grade in new_grades:
                    config.DB.insert('grades', grade=grade)

                for group in new_groups:
                    config.DB.insert('groups', groupe=group)

    raise web.seeother('/admin/books')




def tickets_get():
    tickets = config.DB.select('tickets')
    # compute total
    total = 0.0
    for item in tickets:
        total = total + float(item['total'])
    tickets = config.DB.select('tickets')
    return render.tickets(tickets, total)

def tickets_post():
    i = web.input()
    for inv_id in i:
        # TODO add items to the stock
        config.DB.delete('tickets', where="id=$inv_id", vars=locals())
    raise web.seeother('/admin/tickets')



def ticket_get(id):
    itemlist = list()
    # get ORG and NIF from 'users'
    org = 'ORG'
    org = config.DB.select('users', where="username = $org limit 1", vars=locals()).list();
    nif = 'NIF'
    nif = config.DB.select('users', where="username = $nif limit 1", vars=locals()).list();
    # get books IDs
    ticket = config.DB.select('tickets', where="id=$id limit 1", vars=locals())
    stritems = ticket[0]['libros']
    splited = stritems.split(', ')
    # sort books IDs
    res = map(int, splited)
    for i in map(str, sorted(res)):
        itemlist.append(config.DB.select('books', where="id = $i limit 1", vars=locals()).list())
    # get ticket
    ticket = config.DB.select('tickets', where="id=$id limit 1", vars=locals())
    return render.printandarchive(ticket[0], itemlist, org[0], nif[0], enabled=False)



def backup_get():
    return render.backup()

def backup_post():
    x = web.input(myfile={})
    if 'myfile' in x:
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        shutil.copy2('db/libros.sqlite', 'db/libros-' + timestamp + '.sqlite')
        filename = 'db/libros.sqlite'
        # creates the file where the uploaded file should be stored
        fout = open(filename,'w')
        # writes the uploaded file to the newly created file.
        fout.write(x.myfile.file.read())
        # closes the file, upload complete.
        fout.close()
    raise web.seeother('/admin')
