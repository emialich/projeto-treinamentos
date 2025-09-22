import pytest
import json


class TestAlunosRoutes:
    """Testes para as rotas de alunos."""
    
    def test_get_alunos_vazio(self, client):
        """Testa GET quando não há alunos."""
        response = client.get('/alunos/')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_alunos_com_dados(self, client, aluno_sample):
        """Testa GET com alunos existentes."""
        response = client.get('/alunos/')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['nome'] == "Maria Santos"
        assert response.json[0]['email'] == "maria@email.com"
    
    def test_criar_aluno_sucesso(self, client, turma_sample, treinamento_sample):
        """Testa criação de aluno com sucesso."""
        dados = {
            "nome": "João Pedro",
            "email": "joao@email.com",
            "treinamento_id": treinamento_sample.id,
            "pago": True
        }
        response = client.post('/alunos/',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['nome'] == "João Pedro"
        assert response.json['email'] == "joao@email.com"
        assert response.json['pago'] is True
    
    def test_criar_aluno_dados_incompletos(self, client):
        """Testa criação com dados obrigatórios ausentes."""
        dados = {"nome": "Teste"}
        response = client.post('/alunos/',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 400
        assert "Dados incompletos" in response.json['erro']
    
    def test_criar_aluno_treinamento_inexistente(self, client):
        """Testa criação com treinamento inexistente."""
        dados = {
            "nome": "Teste Silva",
            "email": "teste@email.com",
            "treinamento_id": 999
        }
        response = client.post('/alunos/',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 500
        assert "não foi encontrado" in response.json['erro']
    
    def test_criar_aluno_email_duplicado(self, client, aluno_sample, treinamento_sample):
        """Testa criação com email já existente."""
        dados = {
            "nome": "Outro Nome",
            "email": "maria@email.com",  # Email já usado no aluno_sample
            "treinamento_id": treinamento_sample.id
        }
        response = client.post('/alunos/',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 500
        assert "Não foi possível criar o aluno" in response.json['erro']
    
    def test_criar_aluno_sem_pago_default_false(self, client, treinamento_sample):
        """Testa que campo 'pago' tem default False."""
        dados = {
            "nome": "Ana Costa",
            "email": "ana@email.com",
            "treinamento_id": treinamento_sample.id
        }
        response = client.post('/alunos/',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['pago'] is False
    
    def test_criar_aluno_corpo_vazio(self, client):
        """Testa criação com corpo da requisição vazio."""
        response = client.post('/alunos/',
                             data='',
                             content_type='application/json')
        
        assert response.status_code == 400
        assert "Dados incompletos" in response.json['erro']