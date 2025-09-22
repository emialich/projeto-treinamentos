import pytest
import os
from app import create_app, db
from app.models.treinamentos import Treinamento
from app.models.turmas import Turma
from app.models.alunos import Aluno
from datetime import date


@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes."""
    # Configura variáveis de ambiente para teste
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de teste para fazer requisições."""
    return app.test_client()


@pytest.fixture
def treinamento_sample(app):
    """Cria um treinamento de exemplo."""
    with app.app_context():
        treinamento = Treinamento(
            nome_treinamento="Python Básico",
            vendor="TechCorp",
            instrutor_sugerido="João Silva"
        )
        db.session.add(treinamento)
        db.session.commit()
        return treinamento


@pytest.fixture
def turma_sample(app, treinamento_sample):
    """Cria uma turma de exemplo."""
    with app.app_context():
        turma = Turma(
            treinamento_id=treinamento_sample.id,
            data_inicio=date(2024, 6, 15),
            horario="09:00 - 17:00",
            local="Sala 1",
            status="Agendada"
        )
        db.session.add(turma)
        db.session.commit()
        return turma


@pytest.fixture
def aluno_sample(app, turma_sample):
    """Cria um aluno de exemplo."""
    with app.app_context():
        aluno = Aluno(
            nome="Maria Santos",
            email="maria@email.com",
            turma_id=turma_sample.id,
            pago=False
        )
        db.session.add(aluno)
        db.session.commit()
        return aluno