import secrets, os
from flask import redirect, url_for, render_template, request, flash, session, current_app, make_response
from flask_bcrypt import Bcrypt
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroClienteForm, LoginClienteForm
from .models import Cadastrar, ClientePedido
from flask_login import login_user, current_user, logout_user, login_required
from weasyprint import HTML
import stripe


publishable_key = 'pk_test_51QJx6TGjTd6wOkkdfE6OGOzgB8Vqj3ngPZ90qMeUpo26NDIBsoRhL52PnpeU6FQfjKCVeGHK0AHEl0YrrfXrFnGc007KIrqJp0'
stripe.api_key = 'sk_test_51QJx6TGjTd6wOkkdBXslNJRRNnEegTl9kpkZNVJThbPRjYlklwOsHHtJ6JgIDCKfySfCoYt1KgAm9a1YkprrujiR00ysLw3vQT'



@app.route('/pagamento', methods=['POST'])
@login_required
def pagamento():
    notafiscal = request.form.get('invoice')
    total = request.form.get('total')
    total_centavos = int(float(total) * 100)

    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    charge = stripe.Charge.create(customer=customer.id, amount=total_centavos, currency='usd', description='The Product')
    #pedido_order = pedido_order.query.filter_by(cliente_id=current_user.id).order_by(ClientePedido.id.desc()).first()
    cliente_pedido = ClientePedido.query.filter_by(cliente_id=current_user.id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
    cliente_pedido.status = 'Pago'
    db.session.commit()


    return redirect(url_for('obrigado'))





@app.route('/obrigado')
def obrigado():
    return render_template('cliente/obrigado.html')


@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = CadastroClienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, country=form.country.data, state=form.state.data, city=form.city.data, address=form.address.data, zipcode=form.zipcode.data, contact=form.contact.data, profile='profile.jpg')
        db.session.add(cadastrar)
        flash(f' Obriagdo {form.name.data} por se cadastrar', 'success')
        db.session.commit()
        # return redirect(url_for('login')) bug
        return redirect(url_for('clientelogin'))
    return render_template('cliente/cliente.html', form=form)


@app.route('/cliente/login', methods=['GET', 'POST'])
def clientelogin():
    form = LoginClienteForm()
    if form.validate_on_submit():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login não realizado. Por favor, verifique seu email e senha', 'danger')

    return render_template('cliente/login.html', form=form)


@app.route('/cliente/logout')
def clientelogout():
    logout_user()
    return redirect(url_for('home'))



def atualizarlojaCarro():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        del produto['image']
        del produto['colors']

    return atualizarlojaCarro
        


@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        atualizarlojaCarro()

        try:
            p_order = ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash('Pedido realizado com sucesso!', 'success')
            return redirect(url_for('pedidos', notafiscal=notafiscal))
        except Exception as e:
            print(e)
            flash('Algo deu errado ao fazer o pedido', 'danger')
            return redirect(url_for('getCart'))


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


@app.route('/get_pdf/<notafiscal>', methods=['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated:
        subTotal = 0
        gTotal = 0
        cliente_id = current_user.id
        if request.method == 'POST':
            cliente = Cadastrar.query.filter_by(id=cliente_id).first()
            pedido_order = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key, produto in pedido_order.pedido.items():
                desconto = (produto.get('discount') / 100) * float(produto.get('price'))
                subTotal += float(produto.get('price')) * int(produto.get('quantity'))
                subTotal -= desconto
                gTotal = float("%.2f" % (1 * subTotal))

            rendered = render_template('cliente/pdf.html', notafiscal=notafiscal, cliente=cliente, pedido_order=pedido_order, subTotal=subTotal, gTotal=gTotal)
            try:
                pdf = HTML(string=rendered).write_pdf()
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf'
                #response.headers['Content-Disposition'] = f'inline; filename=pedido_{notafiscal}.pdf'
                response.headers['Content-Disposition'] = f'attachment; filename=pedido_{notafiscal}.pdf'
                return response
            except Exception as e:
                print(f"Erro ao gerar PDF: {e}")
                return f"Erro ao gerar PDF: {e}"  # Isso ajudará a ver o erro específico no navegador

    else:
        return redirect(url_for('pedidos'))