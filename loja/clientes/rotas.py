import secrets, os
from flask import redirect, url_for, render_template, request, flash, session, current_app
from loja import db, app, photos
from .forms import CadastroClienteForm

@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastrar_clientes():
    form = CadastroClienteForm(request.form)
    return render_template('cliente/cliente.html', form=form)



