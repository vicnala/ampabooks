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
    return render.login(login_form, datetime.now(), allow = True)

def login_post(session):
    if not login_form.validates(): 
        return render.login(login_form, datetime.now(), allow = True)
    else:
        allowed = config.DB.select('users').list()
        for i in allowed:
            if login_form.d.usuario == i.username:
                session.logged_in = True
                session.name = i.name
                session.username = i.username
                raise web.seeother('/search')
        return render.login(login_form, datetime.now(), allow = False)

