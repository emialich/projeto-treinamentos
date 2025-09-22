# 👨‍💻 Guia de Desenvolvimento

## Configuração do Ambiente

### 1. Ambiente de Desenvolvimento
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências de desenvolvimento
pip install -r requirements.txt

# Configurar Flask para desenvolvimento
set FLASK_ENV=development
set FLASK_APP=run.py
```

### 2. Executar em Modo Debug
```bash
python run.py
```

## Estrutura de Desenvolvimento

### Adicionando Novos Modelos

1. Criar arquivo em `app/models/`
2. Importar em `app/__init__.py`
3. Gerar migração:
```bash
flask db migrate -m "Adicionar modelo X"
flask db upgrade
```

### Adicionando Novas Rotas

1. Criar blueprint em `app/routes/`
2. Registrar em `app/__init__.py`:
```python
from .routes.novo_modulo import novo_bp
app.register_blueprint(novo_bp, url_prefix='/novo')
```

### Padrão de Rotas
```python
from flask import Blueprint, jsonify, request
from app.models.modelo import Modelo
from app.database import db

modulo_bp = Blueprint('modulo', __name__)

@modulo_bp.route('/', methods=['GET'])
def listar():
    items = Modelo.query.all()
    return jsonify([item.to_dict() for item in items])

@modulo_bp.route('/', methods=['POST'])
def criar():
    dados = request.get_json()
    # Validações
    # Criação
    # Retorno
```

## Testes

### Executar Testes
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_models.py

# Com cobertura
pytest --cov=app
```

### Criar Novos Testes
```python
def test_nova_funcionalidade(client, fixture_sample):
    response = client.post('/endpoint', json={...})
    assert response.status_code == 201
    assert response.json['campo'] == 'valor'
```

## Banco de Dados

### Migrações
```bash
# Criar migração
flask db migrate -m "Descrição da mudança"

# Aplicar migração
flask db upgrade

# Reverter migração
flask db downgrade
```

### Comandos Úteis
```bash
# Ver histórico
flask db history

# Ver migração atual
flask db current

# Resetar banco (cuidado!)
flask db downgrade base
flask db upgrade
```

## Debugging

### Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug('Mensagem de debug')
```

### Breakpoints
```python
import pdb; pdb.set_trace()
```

### Flask Debug Toolbar
```python
# Em desenvolvimento
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)
```

## Boas Práticas

### Código
- Use type hints quando possível
- Docstrings em funções complexas
- Nomes descritivos para variáveis
- Máximo 80 caracteres por linha

### Commits
```bash
git commit -m "feat: adicionar endpoint de relatórios"
git commit -m "fix: corrigir validação de email"
git commit -m "docs: atualizar README"
```

### Testes
- Um teste por funcionalidade
- Nomes descritivos
- Arrange, Act, Assert
- Mocks para dependências externas

## Ferramentas Úteis

### Formatação
```bash
pip install black flake8
black app/
flake8 app/
```

### Postman/Insomnia
Importe a collection da API para testes manuais.

### VS Code Extensions
- Python
- Flask Snippets
- SQLAlchemy
- GitLens

## Deploy

### Preparação
```bash
# Gerar requirements.txt
pip freeze > requirements.txt

# Variáveis de produção
FLASK_ENV=production
DATABASE_URL=postgresql://...
```

### Docker
```bash
# Build
docker build -t treinamentos-api .

# Run
docker run -p 5000:5000 treinamentos-api
```