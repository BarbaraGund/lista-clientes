# models.py
# Define o modelo (tabela) Cliente usando SQLAlchemy.

from flask_sqlalchemy import SQLAlchemy
import warnings

# Ignorar avisos do SQLAlchemy
warnings.filterwarnings('ignore')

# Instância do SQLAlchemy que será inicializada no app.py
db = SQLAlchemy()


class Cliente(db.Model):
    """Representa a tabela 'cliente' no banco de dados."""

    __tablename__ = 'cliente'

    # Campos obrigatórios do cliente
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    cpf = db.Column(db.String(11), nullable=False, unique=True)

    def __repr__(self):
        return f'<Cliente {self.id} - {self.nome}>'

