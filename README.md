# CRUD de Clientes - Flask + SQLAlchemy

Projeto simples de gerenciamento de clientes (Cadastrar, Listar, Editar e Excluir),
desenvolvido com Flask e Flask-SQLAlchemy, utilizando banco de dados SQLite.

## Tecnologias

- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.31

## Estrutura do projeto

```
cliente_crud/
├── app.py               # Rotas e lógica da aplicação
├── models.py             # Modelo (tabela) Cliente
├── requirements.txt       # Dependências do projeto
└── templates/
    ├── index.html         # Lista de clientes
    ├── adicionar.html      # Formulário de cadastro
    └── editar.html         # Formulário de edição
```

## Como executar

1. Crie e ative um ambiente virtual (venv):

   No Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   No Linux/Mac:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   python app.py
   ```

4. Acesse no navegador:
   ```
   http://127.0.0.1:5000/
   ```

O banco de dados SQLite (`clientes.db`) será criado automaticamente na primeira
execução, dentro da pasta do projeto.

## Rotas disponíveis

- `GET  /`               -> Lista todos os clientes
- `GET  /adicionar`       -> Formulário de cadastro
- `POST /adicionar`       -> Salva um novo cliente
- `GET  /editar/<id>`     -> Formulário de edição preenchido
- `POST /editar/<id>`     -> Atualiza os dados do cliente
- `GET  /deletar/<id>`    -> Remove o cliente e volta para a lista
