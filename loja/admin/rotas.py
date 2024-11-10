from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Addproduto, Marca, Categoria
from loja import app, db, bcrypt
from .forms import RegistrationForm, LoginFormulario
from .models import User
import os



admin_bp = Blueprint('admin', __name__)

'''
@app.route('/')
def home():
    return redirect(url_for('login'))
'''


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))
    produtos = Addproduto.query.all()
    return render_template('admin/index.html', title="Pagina Administrativa", produtos=produtos, show_banner=True)

@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))
    marcas = Marca.query.order_by(Marca.id.desc()).all()
    return render_template('admin/marca.html', title="Pagina de Fabricantes", marcas=marcas, show_banner=False)


@app.route('/categoria')
def categoria():
    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template('admin/marca.html', title="Pagina de Categorias", categorias=categorias, show_banner=False)
    
        

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,email= form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado por se registrar {form.name.data}!', 'success')
        return redirect(url_for('login')) #mudar para ('login')
    return render_template('admin/registrar.html', form=form, title="Pagina de registros")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginFormulario(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #session['logado'] = True
            session['email'] = form.email.data
            flash(f'Bem vindo {form.email.data}! Você está logado agora', 'success')
            return redirect(request.args.get('next')or  url_for('admin'))
        else:
            flash('Desculpe, email ou senha incorretos', 'danger')
    return render_template('admin/login.html', form=form, title="Pagina de login")
