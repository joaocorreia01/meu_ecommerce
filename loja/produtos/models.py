from loja import db, app

from datetime import datetime

class Addproduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=True)
    marca = db.relationship('Marca', backref=db.backref('marca', lazy=True))

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('produtos', lazy=True)) #observar se é o mesmo nome da tabela

    create_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    image_1 = db.Column(db.String(150), nullable=False, default='default.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='default.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='default.jpg')

    def __repr__(self):
        return f'<Addproduto: {self.name}>'



class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)


with app.app_context():
    db.create_all()