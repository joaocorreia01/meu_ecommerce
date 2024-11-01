from wtforms import Form, BooleanField, StringField, PasswordField, validators

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(Form):
    name = StringField('Nome Completo :', [validators.Length(min=4, max=25)])
    username = StringField('Usuario :', [validators.Length(min=4, max=25)])
    email = StringField('Email :', [validators.Length(min=6, max=35)])
    password = PasswordField('Nova Senha', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Senhas não conferem')
    ])
    confirm = PasswordField('Repita a senha')
    accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])
    

class LoginFormulario(Form):
    email = StringField('Email :', [validators.Length(min=6, max=35)])
    password = PasswordField('Senha :', [validators.DataRequired()])