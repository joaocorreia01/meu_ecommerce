from flask_wtf.file import FileField, FileAllowed, FileRequired
from  wtforms import Form, IntegerField, StringField, TextAreaField, BooleanField, validators

class Addprodutos(Form):
    name = StringField('Nome :', [validators.DataRequired()])
    price = IntegerField('Preco :', [validators.DataRequired()])
    discount = IntegerField('Desconto :', [validators.DataRequired()])
    stock = IntegerField('Estoque :', [validators.DataRequired()])
    description = TextAreaField('Descricao :', [validators.DataRequired()])
    colors = TextAreaField('Cor :', [validators.DataRequired()])

    image_1 = FileField('Imagem 1 :', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Somente imagens são aceitas.')])
    image_2 = FileField('Imagem 2 :', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Somente imagens são aceitas.')])
    image_3 = FileField('Imagem 3 :', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Somente imagens são aceitas.')])    
    
