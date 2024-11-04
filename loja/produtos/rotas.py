from flask import redirect, url_for, render_template, request, flash
from loja import db, app
from .forms import Addprodutos
from .models import Marca, Categoria


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    if request.method == "POST":
        getmarca = request.form.get('marca')
        if getmarca:  # Verifica se getmarca não é None ou vazio
            marca = Marca(name=getmarca)
            db.session.add(marca)
            db.session.commit()
            flash(f'Marca {getmarca} adicionada com sucesso', 'success')
            return redirect(url_for('addmarca'))
        else:
            flash('O campo de marca não pode estar vazio.', 'danger')
    return render_template('/produtos/addmarca.html', marcas=True)


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        if getmarca:  # Verifica se getmarca não é None ou vazio
            cat = Categoria(name=getmarca)
            db.session.add(cat)
            db.session.commit()
            flash(f'Categoria {getmarca} adicionada com sucesso', 'success')
            return redirect(url_for('addcat'))
        else:
            flash('O campo de marca não pode estar vazio.', 'danger')
    return render_template('/produtos/addmarca.html')


@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    form = Addprodutos(request.form)
    return render_template('produtos/addproduto.html', title = "Cadastro de Produto", form=form)