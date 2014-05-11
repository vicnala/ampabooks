import web
import view, config
from view import render

urls = (
    '/', 'index',
    '/search','search',
    '/login','login',
    '/logout','logout',
    '/admin','admin',
    '/grades', 'grades',
    '/gradeadd', 'gradeadd',
    '/groups', 'groups',
    '/groupadd', 'groupadd',
    '/students', 'students',
    '/users','users',
    '/useradd', 'useradd',
    '/libros.css','css',
    '/favicon.ico','favicon',
)

web.config.debug = False
app = web.application(urls, globals())
app.internalerror = web.debugerror
session = web.session.Session(app, web.session.DiskStore('sessions'), {
    'name': None,
    'username': None,
    'logged_in': None
})


class restrict(object):
    # Decorator for user sections of the website that need restriction.
    def __init__(self, request):
        self.__request = request

    def __call__(self, *args, **kwargs):
        if session.logged_in != True:
            web.seeother('/login')
        else:
            return self.__request(self, *args, **kwargs)


class admin_restrict(object):
    # Decorator for admin sections of the website.
    def __init__(self, request):
        self.__request = request

    def __call__(self, *args, **kwargs):
        if session.username != 'admin':
            web.seeother('/')
        else:
            return self.__request(self, *args, **kwargs)


class index:
    @restrict
    def GET(self):
        #return view.listing()
        if session.username != 'admin':
            raise web.seeother('/search')
        raise web.seeother('/admin')


class admin:
    @admin_restrict
    def GET(self):
        return view.admin_get()


class grades:
    @admin_restrict
    def GET(self):
        return view.grades_get()

    @admin_restrict
    def POST(self):
        return view.grades_post()


class gradeadd:
    @admin_restrict
    def GET(self):
        return view.gradeadd_get()

    @admin_restrict
    def POST(self):
        return view.gradeadd_post()



class groups:
    @admin_restrict
    def GET(self):
        return view.groups_get()

    @admin_restrict
    def POST(self):
        return view.groups_post()


class groupadd:
    @admin_restrict
    def GET(self):
        return view.groupadd_get()

    @admin_restrict
    def POST(self):
        return view.groupadd_post()



class users:
    @admin_restrict
    def GET(self):
        return view.users_get()

    @admin_restrict
    def POST(self):
        return view.users_post()


class useradd:
    @admin_restrict
    def GET(self):
        return view.useradd_get()

    @admin_restrict
    def POST(self):
        return view.useradd_post()


class students:
    @admin_restrict
    def GET(self):
        return view.students_get()

    @admin_restrict
    def POST(self):
        return view.students_post()



class search:
    @restrict
    def GET(self):
        return render.search()



class login:
    def GET(self):
        return view.login_get()

    def POST(self):
        return view.login_post(session)


class logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')


class css:
    def GET(self):
        f = open("stylesheets/libros.css", 'rb')
        return f.read()


class favicon:
    def GET(self):
        f = open("images/favicon.ico", 'rb')
        web.header("Content-Type","image/x-icon") 
        return f.read()


if __name__ == "__main__":
    app.run()