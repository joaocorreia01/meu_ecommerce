from loja import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


@login_manager.user_loader
def user_carregar(user_id):
    return Cadastrar.query.get(int(user_id))


class Cadastrar(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Garante autoincremento para id
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    profile = db.Column(db.String(50), nullable=True, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Cadastrar {self.name}>'


class ClientePedido(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notafiscal = db.Column(db.String(50), unique= True, nullable=False)
    status = db.Column(db.String(50), default='pendente', nullable=False)
    cliente_id = db.Column(db.Integer, unique=False, nullable=False)
    data_criado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pedido = db.Column(JsonEcodedDict)

    def __repr__(self):
        return f'<ClientePedido {self.notafiscal}>'





# Comando para criar as tabelas após apagar o banco de dados
with app.app_context():
    db.create_all()

