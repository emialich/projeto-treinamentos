import pytest
import json
from datetime import date


class TestTreinamentosRoutes:
    """Testes para as rotas de treinamentos."""
    
    def test_get_treinamentos_vazio(self, client):
        """Testa GET quando não há treinamentos."""
        response = client.get('/treinamentos')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_treinamentos_com_dados(self, client, treinamento_sample):
        """Testa GET com treinamentos existentes."""
        response = client.get('/treinamentos')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['nome_treinamento'] == "Python Básico"
    
    def test_criar_treinamento_sucesso(self, client):
        """Testa criação de treinamento com sucesso."""
        dados = {
            "nome_treinamento": "Docker Fundamentals",
            "vendor": "Docker Inc",
            "instrutor_sugerido": "Ana Silva"
        }
        response = client.post('/treinamentos', 
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['nome_treinamento'] == "Docker Fundamentals"
        assert response.json['vendor'] == "Docker Inc"
    
    def test_criar_treinamento_dados_incompletos(self, client):
        """Testa criação com dados obrigatórios ausentes."""
        dados = {"nome_treinamento": "Kubernetes"}
        response = client.post('/treinamentos',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 400
        assert "obrigatórios" in response.json['erro']
    
    def test_get_por_vendor(self, client, treinamento_sample):
        """Testa busca por vendor."""
        response = client.get('/treinamentos/TechCorp')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['vendor'] == "TechCorp"
    
    def test_get_por_vendor_inexistente(self, client):
        """Testa busca por vendor que não existe."""
        response = client.get('/treinamentos/VendorInexistente')
        assert response.status_code == 404
    
    def test_remover_treinamento_sucesso(self, client, treinamento_sample):
        """Testa remoção de treinamento."""
        dados = {
            "id": treinamento_sample.id,
            "nome_treinamento": "Python Básico"
        }
        response = client.delete('/treinamentos',
                               data=json.dumps(dados),
                               content_type='application/json')
        
        assert response.status_code == 200
        assert "removido com sucesso" in response.json['mensagem']
    
    def test_remover_treinamento_validacao_falha(self, client, treinamento_sample):
        """Testa remoção com validação cruzada falhando."""
        dados = {
            "id": treinamento_sample.id,
            "nome_treinamento": "Nome Errado"
        }
        response = client.delete('/treinamentos',
                               data=json.dumps(dados),
                               content_type='application/json')
        
        assert response.status_code == 400
        assert "Validação falhou" in response.json['erro']


class TestTurmasRoutes:
    """Testes para as rotas de turmas (agendamentos)."""
    
    def test_agendar_treinamento_sucesso(self, client, treinamento_sample):
        """Testa agendamento de nova turma."""
        dados = {
            "treinamento_id": treinamento_sample.id,
            "data_inicio": "2024-08-15",
            "horario": "09:00 - 17:00",
            "local": "Sala 2",
            "status": "Agendada"
        }
        response = client.post('/treinamentos/agendados',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['treinamento_id'] == treinamento_sample.id
        assert response.json['data_inicio'] == "2024-08-15"
    
    def test_agendar_treinamento_inexistente(self, client):
        """Testa agendamento com treinamento inexistente."""
        dados = {
            "treinamento_id": 999,
            "data_inicio": "2024-08-15"
        }
        response = client.post('/treinamentos/agendados',
                             data=json.dumps(dados),
                             content_type='application/json')
        
        assert response.status_code == 404
        assert "não existe no catálogo" in response.json['erro']
    
    def test_get_agendados(self, client, turma_sample):
        """Testa listagem de turmas agendadas."""
        response = client.get('/treinamentos/agendados')
        assert response.status_code == 200
        assert len(response.json) >= 1
    
    def test_atualizar_turma_sucesso(self, client, turma_sample):
        """Testa atualização de turma."""
        dados = {"status": "Cancelada"}
        response = client.put(f'/treinamentos/agendados/{turma_sample.id}',
                            data=json.dumps(dados),
                            content_type='application/json')
        
        assert response.status_code == 200
        assert response.json['status'] == "Cancelada"
    
    def test_atualizar_turma_inexistente(self, client):
        """Testa atualização de turma inexistente."""
        dados = {"status": "Cancelada"}
        response = client.put('/treinamentos/agendados/999',
                            data=json.dumps(dados),
                            content_type='application/json')
        
        assert response.status_code == 404