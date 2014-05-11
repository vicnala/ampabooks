import web
import db
import config
from datetime import datetime
from forms import login_form, useradd_form, gradeadd_form, groupadd_form

import sys

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
    return render.students()
