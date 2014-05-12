import web
import db
import config
from datetime import datetime
from forms import login_form, useradd_form, gradeadd_form, groupadd_form, addstud_form


t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', cache=config.cache, 
    globals=t_globals, base='layout')

render._keywords['globals']['render'] = render


def listing(**k):
    l = db.listing(**k)
    return render.listing(l)



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


grades = []
groups = []

def studadd_get():
    db_grades = config.DB.select('grades')
    for grade in db_grades:
        grades.append((grade.grade, grade.grade))

    db_groups = config.DB.select('groups')
    for group in db_groups:
        groups.append((group.groupe, group.groupe))
    f = addstud_form(grades, groups)
    return render.studadd(f)

def studadd_post():
    f = addstud_form(grades, groups)
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
