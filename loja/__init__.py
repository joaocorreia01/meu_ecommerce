from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from flask_migrate import Migrate



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "meu_ecommerce.db")

app.config['SECRET_KEY'] = 'mysecretkey1234'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
configure_uploads(app, photos)



migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
        

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'clientelogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = "Faça login para acessar esta página."


from loja.admin import rotas
from loja.admin.rotas import admin_bp
from loja.produtos import rotas
from loja.carrinho import carrinhos
from loja.clientes import rotas
app.register_blueprint(admin_bp)
