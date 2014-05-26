import web
import view, config, login, admin
from render import render

urls = (
    '/', 'index',
    '/search','search',
    '/mode','mode',
    '/results','results',
    '/cart','cart',
    '/print','printandarchive',
    '/login','_login',
    '/logout','logout',
    '/admin','_admin',
    '/admin/(grades|gradeadd|groups|groupadd|students|studadd|studexport|' +
        'studimport|books|bookadd|bookexport|bookimport|tickets|users|useradd|' +
        'backup)', '_admins',
    '/studedit/(.*)', 'studedit',
    '/bookedit/(.*)', 'bookedit',
    '/ticket/(.*)','ticket',
    '/useredit/(.*)', 'useredit',
    '/libros.sqlite', 'database',
    '/libros-vacia.sqlite', 'blank_database',    
    '/libros.css','css',
    '/favicon.ico','favicon',
    '/LICENSE', 'license'
)

web.config.debug = False
app = web.application(urls, globals())
app.internalerror = web.debugerror
session = web.session.Session(app, web.session.DiskStore('sessions'), {
    'name': None,
    'username': None,
    'mode': 0,
    'term': None,
    'studid': None,
    'items' : [],
    'dbitems' : [],
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
        session.mode = 0
        return view.index_get(session)


class search:
    @restrict
    def GET(self):
        return view.search_get(session)

    @restrict
    def POST(self):
        return view.search_post(session)


class mode:
    def GET(self):
        session.mode = not session.mode
        raise web.seeother('/search')



class results:
    @restrict
    def GET(self):
        return view.results_get(session)
    
    @restrict
    def POST(self):
        return view.results_post(session)


class cart:
    @restrict
    def GET(self):
        return view.cart_get(session)

    @restrict
    def POST(self):
        return view.cart_post(session)


class printandarchive:
    @restrict
    def GET(self):
        return view.printandarchive(session)


class _admin:
    @admin_restrict
    def GET(self):
        return admin.admin_get()



class _admins:
    @admin_restrict
    def GET(self, param):
        if param == 'grades':
            return admin.grades_get()
        elif param == 'gradeadd':
            return admin.gradeadd_get()
        elif param == 'groups':
            return admin.groups_get()
        elif param == 'groupadd':
            return admin.groupadd_get()
        elif param == 'users':
            return admin.users_get()
        elif param == 'useradd':
            return admin.useradd_get()
        elif param == 'students':
            return admin.students_get()
        elif param == 'studadd':
            return admin.studadd_get()
        elif param == 'studexport':
            return admin.studexport_get()
        elif param == 'studimport':
            return admin.studimport_get()
        elif param == 'books':
            return admin.books_get()
        elif param == 'bookadd':
            return admin.bookadd_get()
        elif param == 'bookexport':
            return admin.bookexport_get()
        elif param == 'bookimport':
            return admin.bookimport_get()
        elif param == 'tickets':
            return admin.tickets_get()
        elif param == 'backup':
            return admin.backup_get()  

    def POST(self, param):
        if param == 'grades':
            return admin.grades_post()
        elif param == 'gradeadd':
            return admin.gradeadd_post()
        elif param == 'groups':
            return admin.groups_post()
        elif param == 'groupadd':
            return admin.groupadd_post()
        elif param == 'users':
            return admin.users_post()
        elif param == 'useradd':
            return admin.useradd_post()
        elif param == 'students':
            return admin.students_post()
        elif param == 'studadd':
            return admin.studadd_post()
        elif param == 'studexport':
            return admin.studexport_post()
        elif param == 'studimport':
            return admin.studimport_post()
        elif param == 'books':
            return admin.books_post()
        elif param == 'bookadd':
            return admin.bookadd_post()
        elif param == 'bookexport':
            return admin.bookexport_post()
        elif param == 'bookimport':
            return admin.bookimport_post()
        elif param == 'tickets':
            return admin.tickets_post()
        elif param == 'backup':
            return admin.backup_post()


class useredit:
    @admin_restrict
    def GET(self, _id):
        return admin.useredit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return admin.useredit_post(web.websafe(_id))


class studedit:
    @admin_restrict
    def GET(self, _id):
        return admin.studedit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return admin.studedit_post(web.websafe(_id))


class bookedit:
    @admin_restrict
    def GET(self, _id):
        return admin.bookedit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return admin.bookedit_post(web.websafe(_id))


class database:
    @admin_restrict
    def GET(self):
        f = open("libros.sqlite", 'rb')
        return f.read()


class blank_database:
    @admin_restrict
    def GET(self):
        f = open("libros-vacia.sqlite", 'rb')
        return f.read()



class _login:
    def GET(self):
        return login.get()

    def POST(self):
        return login.post(session)


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


class license:
    def GET(self):
        f = open("LICENSE", 'rb')
        return f.read() 



if __name__ == "__main__":
    app.run()