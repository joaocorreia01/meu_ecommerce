from wtforms import Form, StringField, validators, IntegerField,StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField,ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from.models import Cadastrar


class CadastroClienteForm(FlaskForm):
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

    def validate_username(self, username):
        if Cadastrar.query.filter_by(username=username.data).first():
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro nome de usuário.')
    
    def validate_email(self, email):
        if Cadastrar.query.filter_by(email=email.data).first():
            raise ValidationError('Este email já está em uso. Por favor, escolha outro email.')