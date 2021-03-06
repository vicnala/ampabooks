import web
import config
from datetime import datetime
from forms import login_form
from render import render

def get():
    return render.login(login_form, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), allow = True)

def post(session):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not login_form.validates(): 
        return render.login(login_form, date_time, allow = True)
    else:
        if login_form.d.usuario == 'admin':
            session.logged_in = True
            session.username = "admin"
            session.name = "Administrador"
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
