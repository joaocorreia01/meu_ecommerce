# meu_ecommerce
Repositório usado na disciplina de Engenharia de Software e Banco de Dados.


## Funcionalidades

### Administração

**1-Cadastro de Usuário Admin e Login:**
- Tela de login para administrador;
- Validação de autenticação (login/logout);
- Página de registro para administrador.

**2-Gerenciamento de Produtos:**
- Cadastro, leitura, atualização e exclusão de produtos (CRUD completo);
- Listagem de produtos na página administrativa;
- Vinculação de produtos a marcas e categorias.

**3-Gerenciamento de Marcas e Categorias:**
- Cadastro, leitura, atualização e exclusão de marcas;
- Cadastro, leitura, atualização e exclusão de categorias;
- Páginas para listagem de marcas e categorias.

**4-Painel Administrativo:**
- Interface centralizada para gerenciar o sistema;
- Exibição de lista de produtos, marcas e categorias no painel.

**5-Mensagens de Feedback:**
- Implementação de mensagens de erro e feedback amigáveis.


### Cliente

**6-Cadastro e Login de Clientes:**
- Tela de login para clientes;
- Cadastro de novos usuários (clientes).

**7-Pagina Inicial:**
- Interface amigável e responsiva para a página home do cliente.

**8-Navegação:**
- Navbar responsiva com links para as seções principais do site.

**9-Busca e Filtro de Produtos:**
- Funcionalidade de pesquisa e filtros para facilitar a busca de produtos.

**10-Página de Detalhes do Produto:**
- Exibição de informações detalhadas de cada produto.


### Carrinho e Checkout

**11-Carrinho de compras:**
- Adição, remoção e edição de produtos no carrinho;

**12-Checkout:**
- Fluxo simples para finalização de compras;
- Sistema básico de pagamento.


### Funcionalidades Extras

**13-Otimização do Sistema:**
- Consultas ao banco de dados otimizadas para maior desempenho.

**14-Geração de Nota Fiscal:**
- Página para geração de notas fiscais das compras realizadas.

**15-Sistema de Pagamento:**
- Integração com um sistema de pagamento básico (Utilizando o stripe);




## Guia de Uso
Este guia ajudará você a configurar e executar o projeto localmente. Siga os passos abaixo:

### Pré-requisitos
Certifique-se de que você tem as seguintes ferramentas instaladas em sua máquina:
- Python (versão 3.10 ou superior);
- Git;
- Um editor de código (como VSCode ou outro de sua preferência).


### Passo 1: Clonar o Repositório
1. Abra um terminal ou prompt de comando.
2. Clone o repositório com o comando:
     ```bash
    git clone https://github.com/joaocorreia01/meu_ecommerce.git

3. Navegue até o diretório do projeto

### Passo 2: Configurar o Ambiente Virtual
1. Crie um ambiente virtual Python:
     ```bash
    python -m venv myenv
2. Ativar o ambiente virtual
- No Windows:
    ```bash
      myenv\Scripts\activate
- No macOS/Linux:
    ```bash
      source myenv/bin/activate
3. Instale as dependências necessárias:
    ```bash
      pip install -r requirements.txt

### Passo 3: Executar o Sistema
1. Certifique-se de que o ambiente virtual está ativado.
2. Execute o arquivo principal do sistema:
     ```bash
    python run.py
3. O servidor será iniciado, e o sistema estará disponível em:
     ```bash
    http://127.0.0.1:5000
4. Acesse o sistema no navegador e utilize as funcionalidades disponíveis!





