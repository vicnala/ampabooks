import web
import db
import config
from datetime import datetime
from forms import login_form


t_globals = dict(
  datestr=web.datestr,
)
render = web.template.render('templates/', cache=config.cache, 
    globals=t_globals, base='layout')
render._keywords['globals']['render'] = render

def listing(**k):
    l = db.listing(**k)
    return render.listing(l)

def login():
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


def admin():
    return render.admin()