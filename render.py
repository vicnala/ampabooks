import web
import config

t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', cache=config.cache, 
    globals=t_globals, base='layout')

render._keywords['globals']['render'] = render
