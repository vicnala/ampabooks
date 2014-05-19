import web
import view, config, login, admin
from render import render
from forms import search_form
from operator import itemgetter
from datetime import datetime

urls = (
    '/', 'index',
    '/search','search',
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
        #print term
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
        total = 0.0
        for item in session.items:
            for i in item:
                total = total + float(i['precio'])
        # get student data
        student = config.DB.select('students', where = "id = $session.studid limit 1", vars=globals())
        return render.preview(student[0], session.items, total, session.name, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


class printandarchive:
    @restrict
    def GET(self):
        # compute total
        del session.dbitems[:]
        total = 0
        for item in session.items:
            for i in item:
                s = int(i['stock'])
                iid = int(i['id'])
                session.dbitems.append(i['id'])
                total = total + float(i['precio'])
                s = s - 1
                # update stock
                config.DB.update('books', where="id = $iid", stock=s, vars=locals())

        
        # sort invoice db items as string
        res = str(sorted(session.dbitems)).strip('[]')
        
        # get student data
        student = config.DB.select('students', where="id = $session.studid limit 1", vars=globals()).list()
        sname = student[0]['nombre']
        grade = student[0]['curso']

        # archive
        config.DB.insert('tickets', dependiente=session.name, alumno=sname, curso=grade, items=res, total=total, date=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

        # get ORG and NIF from 'users'
        org = 'ORG'
        org = config.DB.select('users', where="username = $org limit 1", vars=locals()).list()
        nif = 'NIF'
        nif = config.DB.select('users', where="username = $nif limit 1", vars=locals()).list()

        # print
        invoice = config.DB.select('tickets', order="id desc limit 1").list()
        return render.printandarchive(invoice[0], sorted(session.items, key=lambda k: k[0]['id']), org[0], nif[0], enabled=True)



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


if __name__ == "__main__":
    app.run()