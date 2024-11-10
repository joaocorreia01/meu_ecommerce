import secrets, os
from flask import redirect, url_for, render_template, request, flash, session, current_app
from flask_bcrypt import Bcrypt
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroClienteForm, LoginClienteForm
from .models import Cadastrar, ClientePedido
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login não realizado. Por favor, verifique seu email e senha', 'danger')

    return render_template('cliente/login.html', form=form)


@app.route('/cliente/logout')
def clientelogout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/pedido_order')
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        try:
            p_order = ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash('Pedido realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            flash('Algo deu errado ao fazer o pedido', 'danger')
            return redirect(url_for('getcart'))


@app.route('/pedidos/<notafiscal>')
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated:
        subTotal = 0
        gTotal = 0
        cliente_id = current_user.id
        cliente = Cadastrar.query.filter_by(id=cliente_id).first()
        pedido_order = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
        for _key, produto in pedido_order.pedido.items():
            desconto = (produto.get('discount') / 100) * float(produto.get('price'))
            subTotal += float(produto.get('price')) * int(produto.get('quantity'))
            subTotal -= desconto
            gTotal = float("%.2f" % (1 * subTotal))
    else:
        return redirect(url_for('clientelogin'))

    return render_template('cliente/pedidos.html', notafiscal=notafiscal, cliente=cliente, pedido_order=pedido_order, subTotal=subTotal,gTotal=gTotal)


