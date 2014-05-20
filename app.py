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
    '/grades', 'grades',
    '/gradeadd', 'gradeadd',
    '/groups', 'groups',
    '/groupadd', 'groupadd',
    '/students', 'students',
    '/studadd', 'studadd',
    '/studedit/(.*)', 'studedit',
    '/studexport', 'studexport',
    '/studimport', 'studimport',
    '/books', 'books',
    '/bookadd', 'bookadd',
    '/bookedit/(.*)', 'bookedit',
    '/bookexport', 'bookexport',
    '/bookimport', 'bookimport',
    '/tickets','tickets',
    '/ticket/(.*)','ticket',
    '/users','users',
    '/useradd', 'useradd',
    '/useredit/(.*)', 'useredit',
    '/backup', 'backup',
    '/libros.sqlite', 'database',
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


class grades:
    @admin_restrict
    def GET(self):
        return admin.grades_get()

    @admin_restrict
    def POST(self):
        return admin.grades_post()


class gradeadd:
    @admin_restrict
    def GET(self):
        return admin.gradeadd_get()

    @admin_restrict
    def POST(self):
        return admin.gradeadd_post()



class groups:
    @admin_restrict
    def GET(self):
        return admin.groups_get()

    @admin_restrict
    def POST(self):
        return admin.groups_post()


class groupadd:
    @admin_restrict
    def GET(self):
        return admin.groupadd_get()

    @admin_restrict
    def POST(self):
        return admin.groupadd_post()



class users:
    @admin_restrict
    def GET(self):
        return admin.users_get()

    @admin_restrict
    def POST(self):
        return admin.users_post()


class useradd:
    @admin_restrict
    def GET(self):
        return admin.useradd_get()

    @admin_restrict
    def POST(self):
        return admin.useradd_post()


class useredit:
    @admin_restrict
    def GET(self, _id):
        return admin.useredit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return admin.useredit_post(web.websafe(_id))


class students:
    @admin_restrict
    def GET(self):
        return admin.students_get()

    @admin_restrict
    def POST(self):
        return admin.students_post()


class studadd:
    @admin_restrict
    def GET(self):
        return admin.studadd_get()

    @admin_restrict
    def POST(self):
        return admin.studadd_post()


class studedit:
    @admin_restrict
    def GET(self, _id):
        return admin.studedit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return admin.studedit_post(web.websafe(_id))

class studexport:
    @admin_restrict
    def GET(self):
        return admin.studexport_get()

    @admin_restrict
    def POST(self):
        return admin.studexport_post()


class studimport:
    @admin_restrict
    def GET(self):
        return admin.studimport_get()

    @admin_restrict
    def POST(self):
        return admin.studimport_post()



class books:
    @admin_restrict
    def GET(self):
        return admin.books_get()

    @admin_restrict
    def POST(self):
        return admin.books_post()


class bookadd:
    @admin_restrict
    def GET(self):
        return admin.bookadd_get()

    @admin_restrict
    def POST(self):
        return admin.bookadd_post()


class bookedit:
    @admin_restrict
    def GET(self, _id):
        return admin.bookedit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return admin.bookedit_post(web.websafe(_id))


class bookexport:
    @admin_restrict
    def GET(self):
        return admin.bookexport_get()

    @admin_restrict
    def POST(self):
        return admin.bookexport_post()


class bookimport:
    @admin_restrict
    def GET(self):
        return admin.bookimport_get()

    @admin_restrict
    def POST(self):
        return admin.bookimport_post()



class tickets:
    @admin_restrict
    def GET(self):
        return admin.tickets_get()

    @admin_restrict
    def POST(self):
        return admin.tickets_post()


class ticket:
    @admin_restrict
    def GET(self, id):
        return admin.ticket_get(id)




class backup:
    @admin_restrict
    def GET(self):
        return admin.backup_get()

    @admin_restrict
    def POST(self):
        return admin.backup_post()


class database:
    @admin_restrict
    def GET(self):
        f = open("libros.sqlite", 'rb')
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