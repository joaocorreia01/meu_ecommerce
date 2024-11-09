from flask import redirect, url_for, render_template, request, flash, session, current_app
from loja import db, app
from loja.produtos.models import Addproduto



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
                'color': color,  # Corrigi aqui para utilizar a cor enviada
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
    return render_template('produtos/carros.html', valorapagar=valorapagar)






"""
Usar essa se der merda

@app.route('/carros')
def getCart():
    print("Rota /carros foi acessada")  # Verificação para log

    # Verifica se o carrinho existe na sessão; se não, redireciona para a página inicial
    if 'LojainCarrinho' not in session:
        return redirect(request.referrer or url_for('home'))

    # Passa o conteúdo do carrinho para o template
    return render_template('produtos/carros.html', carrinho=session['LojainCarrinho'])
"""



"""
@app.route('/addCart', methods=['POST'])
def AddCart():
    try:
        produto_id = request.form.get('produto_id')
        quantity = request.form.get('quantidade')
        color = request.form.get('color')
        produto = Addproduto.query.filter_by(id=produto_id).first()

        if produto_id and quantity and color and request.method == 'POST':
            DicItems = {produto_id: {'name': produto.name, 'price': produto.price, 'discount': produto.discount, 'color': produto.color, 'quantity': produto.quantity, 'image': produto.image_1}}
            if 'LojainCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    print("Produto já está no carrinho")
                else:
                    session['LojainCarrinho'] = M_Dicionarios(session['LojainCarrinho'], DicItems)
                    return redirect(request.referrer)
                
            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)


    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
"""
    