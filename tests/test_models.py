import pytest
from datetime import date
from app.models.treinamentos import Treinamento
from app.models.turmas import Turma
from app.models.alunos import Aluno
from app import db


class TestTreinamento:
    """Testes para o modelo Treinamento."""
    
    def test_criar_treinamento(self, app):
        """Testa criação de treinamento."""
        with app.app_context():
            treinamento = Treinamento(
                nome_treinamento="AWS Fundamentals",
                vendor="Amazon",
                instrutor_sugerido="Pedro Costa"
            )
            db.session.add(treinamento)
            db.session.commit()
            
            assert treinamento.id is not None
            assert treinamento.nome_treinamento == "AWS Fundamentals"
            assert treinamento.vendor == "Amazon"
    
    def test_to_dict_treinamento(self, treinamento_sample):
        """Testa conversão para dicionário."""
        result = treinamento_sample.to_dict()
        
        assert 'id' in result
        assert result['nome_treinamento'] == "Python Básico"
        assert result['vendor'] == "TechCorp"
        assert result['instrutor_sugerido'] == "João Silva"


class TestTurma:
    """Testes para o modelo Turma."""
    
    def test_criar_turma(self, app, treinamento_sample):
        """Testa criação de turma."""
        with app.app_context():
            turma = Turma(
                treinamento_id=treinamento_sample.id,
                data_inicio=date(2024, 7, 1),
                horario="14:00 - 18:00",
                local="Online",
                status="Agendada"
            )
            db.session.add(turma)
            db.session.commit()
            
            assert turma.id is not None
            assert turma.treinamento_id == treinamento_sample.id
            assert turma.data_inicio == date(2024, 7, 1)
    
    def test_relacao_treinamento(self, turma_sample, treinamento_sample):
        """Testa relação entre turma e treinamento."""
        assert turma_sample.treinamento.id == treinamento_sample.id
        assert turma_sample.treinamento.nome_treinamento == "Python Básico"


class TestAluno:
    """Testes para o modelo Aluno."""
    
    def test_criar_aluno(self, app, turma_sample):
        """Testa criação de aluno."""
        with app.app_context():
            aluno = Aluno(
                nome="Carlos Silva",
                email="carlos@email.com",
                turma_id=turma_sample.id,
                pago=True
            )
            db.session.add(aluno)
            db.session.commit()
            
            assert aluno.id is not None
            assert aluno.nome == "Carlos Silva"
            assert aluno.email == "carlos@email.com"
            assert aluno.pago is True
    
    def test_email_unico(self, app, turma_sample):
        """Testa constraint de email único."""
        with app.app_context():
            aluno1 = Aluno(
                nome="Ana Costa",
                email="ana@email.com",
                turma_id=turma_sample.id
            )
            db.session.add(aluno1)
            db.session.commit()
            
            # Tenta criar outro aluno com mesmo email
            aluno2 = Aluno(
                nome="Ana Silva",
                email="ana@email.com",
                turma_id=turma_sample.id
            )
            db.session.add(aluno2)
            
            with pytest.raises(Exception):
                db.session.commit()
    
    def test_relacao_turma(self, aluno_sample, turma_sample):
        """Testa relação entre aluno e turma."""
        assert aluno_sample.turma.id == turma_sample.id