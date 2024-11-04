from flask import redirect, url_for, render_template, request, flash
from loja import db, app
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

