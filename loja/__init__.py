from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "meu_ecommerce.db")
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meu_ecommerce.db"
app.config['SECRET_KEY'] = 'mysecretkey1234'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from loja.admin import rotas

# Importa e registra o blueprint
from loja.admin.rotas import admin_bp
from loja.produtos import rotas
app.register_blueprint(admin_bp)
