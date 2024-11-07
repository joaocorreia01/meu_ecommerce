import secrets, os
from flask import redirect, url_for, render_template, request, flash, session, current_app
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
            flash(f'Marca {getmarca} adicionada com sucesso', 'success')
            db.session.commit()
            return redirect(url_for('addmarca'))
        else:
            flash('O campo de marca não pode estar vazio.', 'danger')
    return render_template('/produtos/addmarca.html', marcas=True)


@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
def updatemarca(id):

    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))

    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method == "POST":
        updatemarca.name = marca
        flash(f'Fabricante {marca} atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template('/produtos/updatemarca.html', title="Atualizar Fabricantes", updatemarca=updatemarca)


'''
@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):

    marca = Marca.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(marca)
        db.session.commit()
        flash(f'Fabricante {marca.name} deletado com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'Fabricante {marca.name} não pode ser deletado', 'warning')
    return redirect(url_for('admin'))
'''
#Impedir a Exclusão de Fabricantes com Produtos Associados
@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):
    marca = Marca.query.get_or_404(id)
    if marca.marca:
        flash(f'Não é possível deletar a marca {marca.name} pois existem produtos associados a ela.', 'warning')
        return redirect(url_for('admin'))
    
    db.session.delete(marca)
    db.session.commit()
    flash(f'Fabricante {marca.name} deletado com sucesso', 'success')
    return redirect(url_for('admin'))


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):

    if 'email' not in session:
        flash('Por favor, faça o login para acessar o sistema ', 'danger')
        return redirect(url_for('login'))

    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method == "POST":
        updatecat.name = categoria
        flash(f'Categoria {categoria} atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('categoria')) #observar se é categorias msm

    return render_template('/produtos/updatemarca.html', title="Atualizar Categoria", updatecat=updatecat)


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

@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    categoria = Categoria.query.get_or_404(id)

    '''
    if request.method == "POST":
        db.session.delete(categoria)
        db.session.commit()
        flash(f'Categoria {categoria.name} deletada com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'Categoria {categoria.name} não pode ser deletada', 'warning')
    return redirect(url_for('admin'))
    '''

    if categoria.produtos:
        flash(f'Não é possível deletar a categoria {categoria.name} pois existem produtos associados a ela.', 'warning')
        return redirect(url_for('admin'))
    
    db.session.delete(categoria)
    db.session.commit()
    flash(f'Categoria {categoria.name} deletada com sucesso', 'success')
    return redirect(url_for('admin'))
    


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
        return redirect(url_for('admin'))
    
    return render_template('produtos/addproduto.html', title="Cadastro de Produto", form=form, marcas=marcas, categorias=categorias)

@app.route('/deleteproduto/<int:id>', methods=['POST'])
def deleteproduto(id):
    produto = Addproduto.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
        except Exception as e:
            print(e)
        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto {produto.name} deletado com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'Produto {produto.name} não pode ser deletado', 'warning')
    return redirect(url_for('admin'))

@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])
def updateproduto(id):
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)

    if request.method == "POST":
        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data

        produto.marca_id = marca
        produto.categoria_id = categoria

        produto.stock = form.stock.data
        produto.description = form.description.data
        produto.color = form.colors.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")
        

        db.session.commit()

        flash(f'Produto {produto.name} atualizado com sucesso', 'success')
        
        return redirect(url_for('admin')) #redirect('admin')
    
    form.name.data = produto.name
    form.price.data = produto.price
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.description.data = produto.description
    form.colors.data = produto.color


    return render_template('/produtos/updateproduto.html', title="Atualizar Categoria", form=form, marcas=marcas, categorias=categorias, produto=produto)
