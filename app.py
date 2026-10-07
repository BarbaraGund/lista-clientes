# app.py
# Aplicação Flask responsável pelo CRUD (Create, Read, Update, Delete) de Clientes.
# Utiliza Flask-SQLAlchemy para persistência em um banco SQLite local.

from flask import Flask, render_template, request, redirect, url_for
from models import db, Cliente

# ---------------------------------------------------------------------------
# Configuração da aplicação
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Banco de dados SQLite salvo na raiz do projeto (arquivo clientes.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conecta o SQLAlchemy à aplicação Flask
db.init_app(app)

# Cria as tabelas do banco de dados (caso ainda não existam)
with app.app_context():
    db.create_all()


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------
def validar_cliente(nome, email, cpf):
    """
    Valida os dados básicos do cliente.
    Retorna uma mensagem de erro (string) caso algo esteja inválido,
    ou None caso os dados estejam corretos.
    """
    # Verifica se algum campo obrigatório está vazio
    if not nome or not email or not cpf:
        return 'Todos os campos (Nome, Email e CPF) são obrigatórios.'

    # Validação simples de e-mail
    if '@' not in email or '.' not in email:
        return 'Informe um e-mail válido.'

    # Validação simples de CPF (apenas números, com 11 dígitos)
    cpf_numeros = cpf.replace('.', '').replace('-', '')
    if not cpf_numeros.isdigit() or len(cpf_numeros) != 11:
        return 'CPF inválido. Informe apenas os 11 números do CPF.'

    return None


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Busca todos os clientes no banco e exibe na tela inicial."""
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    """
    GET  -> Exibe o formulário de cadastro de um novo cliente.
    POST -> Valida e tenta salvar o novo cliente no banco de dados.
    """
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        cpf = request.form.get('cpf', '').strip()

        # Valida os campos obrigatórios
        erro = validar_cliente(nome, email, cpf)

        # Verifica se já existe um cliente com o mesmo email ou CPF
        if not erro:
            cliente_existente = Cliente.query.filter(
                (Cliente.email == email) | (Cliente.cpf == cpf)
            ).first()
            if cliente_existente:
                erro = 'Já existe um cliente cadastrado com este e-mail ou CPF.'

        # Se houver erro, recarrega a tela de adicionar mantendo os dados digitados
        if erro:
            return render_template(
                'adicionar.html',
                erro=erro,
                nome=nome,
                email=email,
                cpf=cpf
            )

        # Cria o novo cliente e tenta salvar no banco
        novo_cliente = Cliente(nome=nome, email=email, cpf=cpf)
        try:
            db.session.add(novo_cliente)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template(
                'adicionar.html',
                erro=f'Erro ao salvar o cliente: {e}',
                nome=nome,
                email=email,
                cpf=cpf
            )

        # Sucesso: redireciona para a tela inicial
        return redirect(url_for('index'))

    # Método GET: apenas exibe o formulário vazio
    return render_template('adicionar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """
    GET  -> Busca o cliente pelo id e carrega o formulário de edição preenchido.
    POST -> Valida e tenta atualizar os dados do cliente.
    """
    # Busca o cliente pelo id (retorna erro 404 se não existir)
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        cpf = request.form.get('cpf', '').strip()

        # Valida os campos obrigatórios
        erro = validar_cliente(nome, email, cpf)

        # Verifica se já existe OUTRO cliente com o mesmo email ou CPF
        if not erro:
            cliente_existente = Cliente.query.filter(
                Cliente.id != id,
                (Cliente.email == email) | (Cliente.cpf == cpf)
            ).first()
            if cliente_existente:
                erro = 'Já existe outro cliente cadastrado com este e-mail ou CPF.'

        # Se houver erro, recarrega a tela de edição informando o problema
        if erro:
            cliente_form = {'id': id, 'nome': nome, 'email': email, 'cpf': cpf}
            return render_template('editar.html', erro=erro, cliente=cliente_form)

        # Atualiza os dados do cliente
        cliente.nome = nome
        cliente.email = email
        cliente.cpf = cpf

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template(
                'editar.html',
                erro=f'Erro ao atualizar o cliente: {e}',
                cliente=cliente
            )

        # Sucesso: redireciona para a tela inicial
        return redirect(url_for('index'))

    # Método GET: exibe o formulário preenchido com os dados atuais do cliente
    return render_template('editar.html', cliente=cliente)


@app.route('/deletar/<int:id>')
def deletar(id):
    """Busca o cliente pelo id, remove do banco e volta para a tela inicial."""
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('index'))


# ---------------------------------------------------------------------------
# Execução da aplicação
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
