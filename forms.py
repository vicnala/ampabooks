import web

login_form = web.form.Form(
    web.form.Textbox('usuario', web.form.notnull),
)

