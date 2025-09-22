# Testes da Aplicação

Este diretório contém todos os testes automatizados para a aplicação de gerenciamento de treinamentos.

## Estrutura dos Testes

- `conftest.py` - Configurações e fixtures compartilhadas
- `test_models.py` - Testes dos modelos (Treinamento, Turma, Aluno)
- `test_routes_treinamentos.py` - Testes das rotas de treinamentos e turmas
- `test_routes_alunos.py` - Testes das rotas de alunos
- `test_integration.py` - Testes de integração entre módulos

## Como Executar

### Instalar Dependências
```bash
pip install -r requirements.txt
```

### Executar Todos os Testes
```bash
pytest
```

### Executar Testes Específicos
```bash
# Apenas testes de modelos
pytest tests/test_models.py

# Apenas testes de rotas de treinamentos
pytest tests/test_routes_treinamentos.py

# Apenas testes de integração
pytest tests/test_integration.py
```

### Executar com Cobertura
```bash
pytest --cov=app --cov-report=html
```

### Executar Testes Verbosos
```bash
pytest -v
```

## Fixtures Disponíveis

- `app` - Instância da aplicação Flask para testes
- `client` - Cliente de teste para fazer requisições HTTP
- `treinamento_sample` - Treinamento de exemplo
- `turma_sample` - Turma de exemplo
- `aluno_sample` - Aluno de exemplo

## Cobertura dos Testes

Os testes cobrem:

### Modelos
- Criação de objetos
- Validações de campos
- Relacionamentos entre modelos
- Conversão para dicionário
- Constraints de banco de dados

### Rotas
- Endpoints GET, POST, PUT, DELETE
- Validação de dados de entrada
- Tratamento de erros
- Códigos de status HTTP corretos
- Formato de resposta JSON

### Integração
- Fluxos completos de uso
- Relacionamentos entre entidades
- Regras de negócio
- Consistência de dados

## Banco de Dados de Teste

Os testes usam SQLite em memória, garantindo:
- Isolamento entre testes
- Velocidade de execução
- Não interferência com dados reais