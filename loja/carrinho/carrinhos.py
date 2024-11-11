from flask import redirect, url_for, render_template, request, flash, session, current_app
from loja import db, app
from loja.produtos.models import Addproduto
from loja.produtos.rotas import marcas, categorias
import json


def M_Dicionarios(dic1,dic2):
    if isinstance(dic1,list) and isinstance(dic2,list):
        return dic1 + dic2
    elif isinstance(dic1,dict) and isinstance(dic2,dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False


@app.route('/addCart', methods=['POST'])
def AddCart():
    try:
        produto_id = request.form.get('produto_id')
        quantity = int(request.form.get('quantidade'))
        color = request.form.get('color')
        produto = Addproduto.query.filter_by(id=produto_id).first()

        if produto_id and quantity and color and request.method == 'POST':
            # Dicionário do item atual
            item = {
                'name': produto.name,
                'price': produto.price,
                'discount': produto.discount,
                'color': color,  # Corrigi aqui para utilizar as cores enviadas
                'quantity': quantity,
                'image': produto.image_1
            }

            # Verifica se o carrinho já existe na sessão
            if 'LojainCarrinho' in session:
                carrinho = session['LojainCarrinho']
                
                # Verifica se o produto já está no carrinho
                if produto_id in carrinho:
                    # Atualiza a quantidade se o produto já existir
                    carrinho[produto_id]['quantity'] += quantity
                    #carrinho[produto_id]['color'] = list(set(carrinho[produto_id]['color'] + color)) #adicionei 14:29 do dia 11/11/24
                else:
                    # Adiciona o produto ao carrinho
                    carrinho[produto_id] = item
                session['LojainCarrinho'] = carrinho
            else:
                # Cria o carrinho com o primeiro item
                session['LojainCarrinho'] = {produto_id: item}

            return redirect(request.referrer)
    except Exception as e:
        print(e)
    return redirect(request.referrer)



@app.route('/carros')
def getCart():
    print("Rota /carros foi acessada")
    if 'LojainCarrinho' not in session:
        return redirect(request.referrer)
    subtotal = 0
    valorapagar = 0
    for key, produto in session['LojainCarrinho'].items():
        desconto = (produto.get('discount') / 100) * float(produto.get('price'))
        subtotal += float(produto.get('price')) * int(produto.get('quantity'))
        subtotal -= desconto
        valorapagar = float("%.2f" % (1 * subtotal))
    return render_template('produtos/carros.html', valorapagar=valorapagar, marcas=marcas(), categorias=categorias())


@app.route('/updateCarro/<int:code>', methods=['POST'])
def updateCarro(code):
    if 'LojainCarrinho' not in session and len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    #item['color'] = list(set(item['color'] + color))
                    flash('Produto atualizado com sucesso', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            flash('Não foi possível atualizar o produto', 'danger')
            return redirect(url_for('getCart'))
    

@app.route('/removeItem/<int:id>')
def removeItem(id):
    if 'LojainCarrinho' not in session and len(session['LojainCarrinho']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            if int(key) == id:
                session['LojainCarrinho'].pop(key, None)
                flash('Produto removido com sucesso', 'success')
                return redirect(url_for('getCart'))
                
    except Exception as e:
        print(e)
        flash('Não foi possível remover o produto', 'danger')
        return redirect(url_for('getCart'))


@app.route('/limparcarro')
def limparcarro():
    try:
        session.pop('LojainCarrinho', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
