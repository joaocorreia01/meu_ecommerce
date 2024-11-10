import secrets, os
from flask import redirect, url_for, render_template, request, flash, session, current_app
from flask_bcrypt import Bcrypt
from loja import db, app, photos, bcrypt
from .forms import CadastroClienteForm
from .models import Cadastrar

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

