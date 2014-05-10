import web

login_form = web.form.Form(
    web.form.Textbox('usuario', web.form.notnull),
)

useradd_form = web.form.Form(
    web.form.Textbox('username', web.form.notnull),
    web.form.Textbox('name', web.form.notnull),
)

gradeadd_form = web.form.Form(
    web.form.Textbox('curso', web.form.notnull),
)