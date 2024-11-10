from wtforms import Form, StringField, validators, IntegerField,StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField
from flask_wtf.file import FileField, FileAllowed



class CadastroClienteForm(Form):
    name = StringField('Nome :')
    username = StringField('Usuario :', [validators.DataRequired()])
    email = StringField('Email :', [validators.DataRequired()])
    password = PasswordField('Senha :', [validators.DataRequired(), validators.EqualTo('confirm', message='Senhas não conferem')])
    confirm = PasswordField('Repita a senha :', [validators.DataRequired()])
    country = StringField('País :', [validators.DataRequired()])
    state = StringField('Estado :', [validators.DataRequired()])
    city = StringField('Cidade :', [validators.DataRequired()])
    address = StringField('Endereço :', [validators.DataRequired()])
    zipcode = StringField('CEP :', [validators.DataRequired()])
    contact = StringField('Contato :', [validators.DataRequired()])
    profile = FileField('Foto de Perfil :', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas fotos!')])
    submit = SubmitField('Cadastrar')