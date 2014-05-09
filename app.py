import web
import view, config
from view import render

urls = (
    '/', 'index',
    '/search','search',
    '/login','login',
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
    """
    Decorator for admin section of the website that need restriction.
    """
    def __init__(self, request):
        self.__request = request

    def __call__(self, *args, **kwargs):
        if session.logged_in != True:
            web.seeother('/login')
        else:
            return self.__request(self, *args, **kwargs)


class index:
    @restrict
    def GET(self):
        #return view.listing()
        raise web.seeother('/search')


class search:
    @restrict
    def GET(self):
        return render.search()


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
    app.run()