import web
import config
from render import render
from forms import search_form
from operator import itemgetter
from datetime import datetime


def index_get(session):
	if session.username != 'admin':
	    raise web.seeother('/search')
	raise web.seeother('/admin')


def search_get(session):
	return render.search(search_form, session.name, session.mode)

def search_post(session):
    if not search_form.validates():
        return render.search(search_form, session.name)
    else:
        session.term = dict(name = "%" + search_form.d.buscar.upper() + "%")
        raise web.seeother('/results')


def results_get(session):
    res = config.DB.select('students', session.term, where = "nombre LIKE $name OR curso LIKE $name")
    return render.results(res, session.name, session.mode)

def results_post(session):
    form = web.input().group
    if form is not None:
        session.studid = form
        raise web.seeother('/studedit/' + session.studid)
        #raise web.seeother('/cart')
    raise web.seeother('/search')


def cart_get(session):
    # get related pack
    student = config.DB.select('students', where = "id = $session.studid limit 1", vars=locals())
    term = dict(curso=student[0].curso)
    student = config.DB.select('students', where = "id = $session.studid limit 1", vars=locals())
    term['grupo'] = student[0].grupo
    #print term
    pack = config.DB.select('books', term, where="curso = $curso AND grupo = 'TODOS' OR curso = $curso AND grupo = $grupo OR curso = 'TODOS' AND grupo = 'TODOS'")
    # get student (again)
    student = config.DB.select('students', where = "id = $session.studid limit 1", vars=locals())
    return render.cart(student[0], pack, session.name, session.mode)


def cart_post(session):
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
            if session.mode:
                total = total - float(i['precio'])
            else:
                total = total + float(i['precio'])

    # get student data
    student = config.DB.select('students', where = "id = $session.studid limit 1", vars=locals())
    return render.preview(student[0], session.items, '{0:.2f}'.format(total), session.name, session.mode, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


def printandarchive(session):
    # compute total
    del session.dbitems[:]
    total = 0
    for item in session.items:
        for i in item:
            s = int(i['stock'])
            iid = int(i['id'])
            session.dbitems.append(i['id'])

            if session.mode:
                total = total - float(i['precio'])
                s = s + 1
            else:
                total = total + float(i['precio'])
                s = s - 1
                # update socio

            # update stock
            config.DB.update('books', where="id = $iid", stock=s, vars=locals())


    # sort ticket db items as string
    res = str(sorted(session.dbitems)).strip('[]')

    # get student data
    student = config.DB.select('students', where="id = $session.studid limit 1", vars=locals()).list()
    sname = student[0]['nombre']
    grade = student[0]['curso']

    # archive
    config.DB.insert('tickets', dependiente=session.name, alumno=sname, curso=grade, libros=res, total=total, date=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    # get ORG and NIF from 'users'
    org = 'ORG'
    org = config.DB.select('users', where="username = $org limit 1", vars=locals()).list()
    nif = 'NIF'
    nif = config.DB.select('users', where="username = $nif limit 1", vars=locals()).list()

    # print
    ticket = config.DB.select('tickets', order="id desc limit 1").list()
    return render.printandarchive(ticket[0], sorted(session.items, key=lambda k: k[0]['id']), org[0], nif[0], enabled=True)
