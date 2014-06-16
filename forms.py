import web

login_form = web.form.Form(
    web.form.Textbox('usuario', web.form.notnull),
)

search_form = web.form.Form(
    web.form.Textbox('buscar', web.form.notnull),
)

useradd_form = web.form.Form(
    web.form.Textbox('username', web.form.notnull),
    web.form.Textbox('name', web.form.notnull),
)

gradeadd_form = web.form.Form(
    web.form.Textbox('curso', web.form.notnull),
)

groupadd_form = web.form.Form(
    web.form.Textbox('grupo', web.form.notnull),
)

def studadd_form (grades, groups):
    f = web.form.Form(
        web.form.Textbox('nombre', web.form.notnull, size=64),
        web.form.Dropdown('curso', grades),
        web.form.Dropdown('grupo', groups),
        web.form.Textbox('tutor', size=64),
        #web.form.Textbox('hermano', size=12),
        web.form.Textbox('tel1', size=12),
        web.form.Textbox('tel2', size=12),
        web.form.Textbox('mail1',size=48),
        web.form.Textbox('mail2', size=48),
    )
    return f


def bookadd_form (grades, groups):
    f = web.form.Form(
        web.form.Textbox('titulo', web.form.notnull, size=64),
        web.form.Dropdown('curso', grades),
        web.form.Dropdown('grupo', groups),
        web.form.Textbox('editorial', size=32),
        web.form.Textbox('isbn', size=32),
        web.form.Textbox('precio', size=12),
        web.form.Textbox('stock', size=12),
    )
    return f