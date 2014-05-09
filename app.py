import web
import view, config
from view import render

urls = (
    '/', 'index',
    '/login','login',
    '/libros.css','css',
    '/favicon.ico','favicon',
)


session = {}


class index:
    def GET(self):
        #return view.listing()
        if session.get('logged_in', False):
            raise web.seeother('/search')
        raise web.seeother('/login')

class login:
    def GET(self):
        return view.login()

    def POST(self):
        return view.login_post(session)


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
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    session = web.session.Session(app, web.session.DiskStore('sessions'), {
        'name': None,
        'username': None,
    })
    app.run()