import web
import view, config
from view import render, search_form
from operator import itemgetter
from datetime import datetime

urls = (
    '/', 'index',
    '/search','search',
    '/results','results',
    '/cart','cart',
    '/login','login',
    '/logout','logout',
    '/admin','admin',
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
    '/users','users',
    '/useradd', 'useradd',
    '/backup', 'backup',
    '/libros.sqlite', 'database',
    '/libros.css','css',
    '/favicon.ico','favicon',
)

web.config.debug = False
app = web.application(urls, globals())
app.internalerror = web.debugerror
session = web.session.Session(app, web.session.DiskStore('sessions'), {
    'name': None,
    'username': None,
    'term': None,
    'studid': None,
    'items' : [],
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


class search:
    @restrict
    def GET(self):
        return render.search(search_form, session.name)

    @restrict
    def POST(self):
        if not search_form.validates(): 
            return render.search(search_form, session.name)
        else:
            session.term = dict(name = "%" + search_form.d.buscar.upper() + "%")
            raise web.seeother('/results')     


class results:
    @restrict
    def GET(self):
        res = config.DB.select('students', session.term, where = "nombre LIKE $name OR curso LIKE $name")
        return render.results(res, session.name)
    
    @restrict
    def POST(self):
        form = web.input().group
        if form is not None:
            session.studid = form
            raise web.seeother('/cart')
        raise web.seeother('/search')



class cart:
    @restrict
    def GET(self):
        # get related pack
        student = config.DB.select('students', where = "id = $session.studid limit 1", vars=globals())
        term = dict(curso=student[0].curso)
        student = config.DB.select('students', where = "id = $session.studid limit 1", vars=globals())
        term['grupo'] = student[0].grupo
        print term
        pack = config.DB.select('books', term, where="curso = $curso AND grupo = 'TODOS' OR curso = $curso AND grupo = $grupo")
        # get student (again)
        student = config.DB.select('students', where = "id = $session.studid limit 1", vars=globals())                
        return render.cart(student[0], pack, session.name)

    @restrict
    def POST(self):
        i = web.input()
        # sort
        isorted = sorted(i, key=itemgetter(0))
        res = map(int, isorted)
        # store
        del session.items[:]
        for prod_id in map(str, sorted(res)):
            session.items.append(config.DB.select('books', where = "id = $prod_id limit 1", vars=locals()).list())
        # compute total
        total = 0
        for item in session.items:
            for i in item:
                total = total + float(i['precio'])
        # get student data
        student = config.DB.select('students', where = "id = $session.studid limit 1", vars=globals())
        return render.preview(student[0], session.items, total, session.name, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


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


class studadd:
    @admin_restrict
    def GET(self):
        return view.studadd_get()

    @admin_restrict
    def POST(self):
        return view.studadd_post()


class studedit:
    @admin_restrict
    def GET(self, _id):
        return view.studedit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return view.studedit_post(web.websafe(_id))

class studexport:
    @admin_restrict
    def GET(self):
        return view.studexport_get()

    @admin_restrict
    def POST(self):
        return view.studexport_post()


class studimport:
    @admin_restrict
    def GET(self):
        return view.studimport_get()

    @admin_restrict
    def POST(self):
        return view.studimport_post()



class books:
    @admin_restrict
    def GET(self):
        return view.books_get()

    @admin_restrict
    def POST(self):
        return view.books_post()


class bookadd:
    @admin_restrict
    def GET(self):
        return view.bookadd_get()

    @admin_restrict
    def POST(self):
        return view.bookadd_post()


class bookedit:
    @admin_restrict
    def GET(self, _id):
        return view.bookedit_get(web.websafe(_id))

    @admin_restrict
    def POST(self, _id):
        return view.bookedit_post(web.websafe(_id))


class bookexport:
    @admin_restrict
    def GET(self):
        return view.bookexport_get()

    @admin_restrict
    def POST(self):
        return view.bookexport_post()


class bookimport:
    @admin_restrict
    def GET(self):
        return view.bookimport_get()

    @admin_restrict
    def POST(self):
        return view.bookimport_post()



class backup:
    @admin_restrict
    def GET(self):
        return view.backup_get()

    @admin_restrict
    def POST(self):
        return view.backup_post()


class database:
    @admin_restrict
    def GET(self):
        f = open("libros.sqlite", 'rb')
        return f.read()



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