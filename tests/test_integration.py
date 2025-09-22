import pytest
import json
from datetime import date


class TestIntegration:
    """Testes de integração entre os módulos."""
    
    def test_fluxo_completo_treinamento(self, client):
        """Testa fluxo completo: criar treinamento -> agendar turma -> inscrever aluno."""
        
        # 1. Criar treinamento no catálogo
        dados_treinamento = {
            "nome_treinamento": "React Avançado",
            "vendor": "Meta",
            "instrutor_sugerido": "Carlos Dev"
        }
        response = client.post('/treinamentos',
                             data=json.dumps(dados_treinamento),
                             content_type='application/json')
        
        assert response.status_code == 201
        treinamento_id = response.json['id']
        
        # 2. Agendar uma turma
        dados_turma = {
            "treinamento_id": treinamento_id,
            "data_inicio": "2024-09-01",
            "horario": "08:00 - 17:00",
            "local": "Lab 1",
            "status": "Agendada"
        }
        response = client.post('/treinamentos/agendados',
                             data=json.dumps(dados_turma),
                             content_type='application/json')
        
        assert response.status_code == 201
        turma_id = response.json['id']
        
        # 3. Inscrever aluno na turma
        dados_aluno = {
            "nome": "Pedro Aluno",
            "email": "pedro@email.com",
            "treinamento_id": treinamento_id,
            "pago": False
        }
        response = client.post('/alunos/',
                             data=json.dumps(dados_aluno),
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['nome'] == "Pedro Aluno"
        
        # 4. Verificar se tudo está conectado
        response = client.get('/treinamentos/agendados')
        turmas = response.json
        assert len(turmas) == 1
        assert turmas[0]['treinamento_info']['nome_treinamento'] == "React Avançado"
    
    def test_nao_pode_remover_treinamento_com_turmas(self, client, treinamento_sample, turma_sample):
        """Testa que não é possível remover treinamento que tem turmas."""
        dados = {
            "id": treinamento_sample.id,
            "nome_treinamento": "Python Básico"
        }
        response = client.delete('/treinamentos',
                               data=json.dumps(dados),
                               content_type='application/json')
        
        assert response.status_code == 409
        assert "já possui turmas agendadas" in response.json['erro']
    
    def test_buscar_treinamentos_por_instrutor(self, client):
        """Testa busca de treinamentos por instrutor."""
        # Criar alguns treinamentos
        treinamentos = [
            {"nome_treinamento": "Python 1", "vendor": "TechA", "instrutor_sugerido": "João Silva"},
            {"nome_treinamento": "Python 2", "vendor": "TechB", "instrutor_sugerido": "João Silva"},
            {"nome_treinamento": "Java 1", "vendor": "TechC", "instrutor_sugerido": "Maria Costa"}
        ]
        
        for dados in treinamentos:
            client.post('/treinamentos',
                       data=json.dumps(dados),
                       content_type='application/json')
        
        # Buscar por instrutor
        response = client.get('/treinamentos/instrutor/João Silva')
        assert response.status_code == 200
        assert len(response.json) == 2
        
        response = client.get('/treinamentos/instrutor/Maria Costa')
        assert response.status_code == 200
        assert len(response.json) == 1
    
    def test_atualizar_status_turma(self, client, turma_sample):
        """Testa atualização de status de turma."""
        # Verificar status inicial
        response = client.get('/treinamentos/agendados')
        turma_inicial = response.json[0]
        assert turma_inicial['status'] == "Agendada"
        
        # Atualizar para "Em andamento"
        dados = {"status": "Em andamento"}
        response = client.put(f'/treinamentos/agendados/{turma_sample.id}',
                            data=json.dumps(dados),
                            content_type='application/json')
        
        assert response.status_code == 200
        assert response.json['status'] == "Em andamento"
        
        # Verificar se foi persistido
        response = client.get('/treinamentos/agendados')
        turma_atualizada = response.json[0]
        assert turma_atualizada['status'] == "Em andamento"
    
    def test_multiplos_alunos_mesma_turma(self, client, turma_sample, treinamento_sample):
        """Testa inscrição de múltiplos alunos na mesma turma."""
        alunos = [
            {"nome": "Aluno 1", "email": "aluno1@email.com"},
            {"nome": "Aluno 2", "email": "aluno2@email.com"},
            {"nome": "Aluno 3", "email": "aluno3@email.com"}
        ]
        
        for dados_aluno in alunos:
            dados_aluno["treinamento_id"] = treinamento_sample.id
            response = client.post('/alunos/',
                                 data=json.dumps(dados_aluno),
                                 content_type='application/json')
            assert response.status_code == 201
        
        # Verificar se todos foram criados
        response = client.get('/alunos/')
        assert len(response.json) >= 3