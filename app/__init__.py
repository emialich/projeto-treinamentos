import os
from flask import Flask
from dotenv import load_dotenv

# Importa a instância 'db' do nosso novo arquivo
from .database import db

# 1. Importa a classe Migrate
from flask_migrate import Migrate

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Cria a instância do Migrate (fora da factory, como o db)
migrate = Migrate()


def create_app():
    # Cria a aplicação Flask
    app = Flask(__name__)

    # Configura o SQLAlchemy a partir do arquivo .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy com a aplicação Flask
    db.init_app(app)

    # 3. Inicializa o Flask-Migrate com a aplicação e o db
    #    É esta linha que adiciona os comandos 'flask db'
    migrate.init_app(app, db)

    # --- Importação dos Modelos ---
    # É fundamental importar os modelos aqui para que o Alembic (motor do Flask-Migrate)
    # saiba da existência das tabelas Aluno, Treinamento e Turma.
    from .models import alunos, treinamentos, turmas

    # Importa e registra os Blueprints
    from .routes.treinamentos import treinamentos_bp
    from .routes.alunos import alunos_bp

    app.register_blueprint(treinamentos_bp, url_prefix='/treinamentos')
    app.register_blueprint(alunos_bp, url_prefix='/alunos')

    return app
