from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_bcrypt import Bcrypt
import os



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "meu_ecommerce.db")
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meu_ecommerce.db"
app.config['SECRET_KEY'] = 'mysecretkey1234'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Define o tamanho máximo de upload (16 MB aqui como exemplo)
configure_uploads(app, photos)


from loja.admin import rotas

# Importa e registra o blueprint
from loja.admin.rotas import admin_bp
from loja.produtos import rotas
from loja.carrinho import carrinhos
app.register_blueprint(admin_bp)
