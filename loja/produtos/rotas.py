import secrets
from flask import redirect, url_for, render_template, request, flash, session
from loja import db, app, photos
from .forms import Addprodutos
from .models import Marca, Categoria, Addproduto




@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():

    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))


    if request.method == "POST":
        getmarca = request.form.get('marca')
        if getmarca:  
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

    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))

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
    return render_template('/produtos/addmarca.html', categoria=True)


@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():

    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()  # Corrigido: renomeado para 'categorias' para ser consistente com o template
    form = Addprodutos(request.form)
    if request.method=="POST":
        
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        color = form.colors.data
        marca= request.form.get('marca')
        categoria = request.form.get('categoria')
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")
        image_2 =photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        image_3 =photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")

        addprod = Addproduto(name=name, price=price, discount=discount, stock=stock, description=description, color=color, marca_id=marca, categoria_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addprod)
        flash(f'Produto {name} adicionado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('login'))

        
    return render_template('produtos/addproduto.html', title="Cadastro de Produto", form=form, marcas=marcas, categorias=categorias)
