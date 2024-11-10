import secrets, os
from flask import redirect, url_for, render_template, request, flash, session, current_app
from flask_bcrypt import Bcrypt
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroClienteForm, LoginClienteForm
from .models import Cadastrar
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = CadastroClienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, country=form.country.data, state=form.state.data, city=form.city.data, address=form.address.data, zipcode=form.zipcode.data, contact=form.contact.data, profile='profile.jpg')
        db.session.add(cadastrar)
        flash(f' Obriagdo {form.name.data} por se cadastrar', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cliente/cliente.html', form=form)


@app.route('/cliente/login', methods=['GET', 'POST'])
def clientelogin():
    form = LoginClienteForm()
    if form.validate_on_submit():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Você está logado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash('Login Inválido. Por favor, verifique o email e a senha', 'danger')
            return redirect(url_for('clientelogin'))
            
    return render_template('cliente/login.html', form=form)

    
