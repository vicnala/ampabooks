import web
import db
import config
from datetime import datetime
from forms import login_form, useradd_form, gradeadd_form, groupadd_form, studadd_form, bookadd_form
import csv
import sqlite3
import os
import shutil

t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', cache=config.cache, 
    globals=t_globals, base='layout')

render._keywords['globals']['render'] = render


def listing(**k):
    l = db.listing(**k)
    return render.listing(l)

grades = []
groups = []

def login_get():
    return render.login(login_form, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), allow = True)

def login_post(session):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not login_form.validates(): 
        return render.login(login_form, date_time, allow = True)
    else:
        if login_form.d.usuario == 'admin':
            session.logged_in = True
            session.username = "admin"
            raise web.seeother('/admin')
        else:
            allowed = config.DB.select('users').list()
            for i in allowed:
                if login_form.d.usuario == i.username:
                    session.logged_in = True
                    session.name = i.name
                    session.username = i.username
                    raise web.seeother('/search')
        return render.login(login_form, date_time, allow = False)



def admin_get():
    return render.admin()



def grades_get():
    grades = config.DB.select('grades')
    return render.grades(grades)

def grades_post():
    i = web.input()
    for grades_id in i:
        config.DB.delete('grades', where="id=$grades_id", vars=locals())
    raise web.seeother('/grades')

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
        raise web.seeother('/grades')



def groups_get():
    groups = config.DB.select('groups')
    return render.groups(groups)

def groups_post():
    i = web.input()
    for groups_id in i:
        config.DB.delete('groups', where="id=$groups_id", vars=locals())
    raise web.seeother('/groups')

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
        raise web.seeother('/groups')




def users_get():
    users = config.DB.select('users')
    return render.users(users)

def users_post():
    i = web.input()
    for user_id in i:
        config.DB.delete('users', where="id=$user_id", vars=locals())
    raise web.seeother('/users')

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
        raise web.seeother('/users')



def students_get():
    students = config.DB.select('students')
    return render.students(students, {})

def students_post():
    i = web.input()
    for key, value in i.items():
        if value in 'on':
            raise web.seeother('/studedit/' + key)


def studadd_get():
    db_grades = config.DB.select('grades')
    for grade in db_grades:
        grades.append((grade.grade, grade.grade))

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
        raise web.seeother('/students')



def studedit_get(_id):
    stud = config.DB.select('students', where="id=$_id", vars=locals())
    if stud is not None:
        db_grades = config.DB.select('grades')
        db_groups = config.DB.select('groups')

        return render.studedit(stud, db_grades, db_groups)
    else:
        raise web.seeother('/students')


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

    raise web.seeother('/students')


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

        with open(fname, 'rb') as data:
            try:
                # csv.DictReader uses first line in file for column headings by default
                dr = csv.DictReader(data) # comma is default delimiter
                to_db = [(i['nombre'], i['curso'], i['grupo'], i['tutor'], i['tel1'],
                         i['tel2'], i['mail1'], i['mail2']) for i in dr]
                os.remove(fname)
            except Exception, e:
                os.remove(fname)
                return render.error('csv.DictReader', e)
            else:
                con = sqlite3.connect('libros.sqlite')
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

    raise web.seeother('/students')




def books_get():
    books = config.DB.select('books')
    return render.books(books, {})

def books_post():
    i = web.input()
    for key, value in i.items():
        if value in 'on':
            raise web.seeother('/bookedit/' + key)


def bookadd_get():
    db_grades = config.DB.select('grades')
    for grade in db_grades:
        grades.append((grade.grade, grade.grade))

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
        config.DB.insert('books', titulo=f.d.titulo, curso=f.d.curso, grupo=f.d.grupo, editorial=f.d.editorial, precio=f.d.precio, stock=f.d.stock)
        raise web.seeother('/books')



def bookedit_get(_id):
    book = config.DB.select('books', where="id=$_id", vars=locals())
    if book is not None:
        db_grades = config.DB.select('grades')
        db_groups = config.DB.select('groups')

        return render.bookedit(book, db_grades, db_groups)
    else:
        raise web.seeother('/books')


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
            editorial=data['editorial'], precio=data['precio'], stock=int(data['stock']),
            grupo=data['grupo'], vars=locals())

    raise web.seeother('/books')


def bookexport_get():
    books = config.DB.select('books')
    data = []
    data.append('titulo,curso,grupo,editorial,precio,stock')
    for book in books:
        row = []
        row.append(book['titulo'])
        row.append(book['curso'])
        row.append(book['grupo'])
        row.append(book['editorial'])
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

        with open(fname, 'rb') as data:
            try:
                # csv.DictReader uses first line in file for column headings by default
                dr = csv.DictReader(data) # comma is default delimiter
                to_db = [(i['titulo'], i['curso'], i['grupo'], i['editorial'], i['precio'],
                         i['stock']) for i in dr]
                os.remove(fname)
            except Exception, e:
                os.remove(fname)
                return render.error('csv.DictReader', e)
            else:
                con = sqlite3.connect('libros.sqlite')
                con.text_factory = str
                cur = con.cursor()
                try:
                    cur.executemany('''INSERT INTO books (titulo, curso, grupo, editorial, 
                                        precio, stock)
                                        VALUES (?, ?, ?, ?, ?, ?);''',
                                        to_db)
                    con.commit()
                except Exception, e:
                    return render.error('SQLite', e)

    raise web.seeother('/books')



def backup_get():
    return render.backup()

def backup_post():
    x = web.input(myfile={})
    if 'myfile' in x:
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        shutil.copy2('libros.sqlite', 'libros-' + timestamp + '-' + '.sqlite')
        # replaces the windows-style slashes with linux ones.
        filepath = x.myfile.filename.replace('\\','/') 
        # splits the and chooses the last part (the filename with extension)
        filename = filepath.split('/')[-1]
        # creates the file where the uploaded file should be stored
        fout = open(filename,'w')
        # writes the uploaded file to the newly created file.
        fout.write(x.myfile.file.read())
        # closes the file, upload complete.
        fout.close()
    raise web.seeother('/admin')
