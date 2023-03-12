from wtforms import Form, StringField, IntegerField, EmailField, validators

class AlumnForm(Form):
    id = IntegerField('id')
    nombre = StringField('nombre')
    apellidos = StringField('apellidos')
    grupo = StringField('grupo')
    email = EmailField('correo')

class MaesForm(Form):
    id = IntegerField('id')
    nombre = StringField('nombre')
    apellidos = StringField('apellidos')
    materia = StringField('materia')
    email = EmailField('correo')