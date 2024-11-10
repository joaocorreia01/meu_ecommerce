from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager



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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'clientelogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = "Faça login para acessar esta página."


from loja.admin import rotas

# Importa e registra o blueprint
from loja.admin.rotas import admin_bp
from loja.produtos import rotas
from loja.carrinho import carrinhos
from loja.clientes import rotas
app.register_blueprint(admin_bp)
