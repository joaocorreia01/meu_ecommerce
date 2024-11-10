from loja import app, db
from datetime import datetime

class Cadastrar(db.Model):
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

# Comando para criar as tabelas após apagar o banco de dados
with app.app_context():
    db.create_all()

