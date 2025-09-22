# 📚 Sistema de Gerenciamento de Treinamentos

Uma API REST desenvolvida em Flask para gerenciar treinamentos corporativos, turmas e alunos.

## 🚀 Funcionalidades

- **Catálogo de Treinamentos**: Gerenciar cursos disponíveis
- **Agendamento de Turmas**: Criar turmas específicas para treinamentos
- **Gestão de Alunos**: Inscrever alunos em turmas específicas
- **Relacionamentos**: Sistema completo de relacionamentos entre entidades

## 🏗️ Arquitetura

```
app/
├── models/          # Modelos de dados (SQLAlchemy)
├── routes/          # Rotas da API (Blueprints)
├── services/        # Lógica de negócio
├── utils/           # Utilitários
└── database.py      # Configuração do banco
```

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- Docker (opcional)

## ⚡ Instalação Rápida

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd notes_project
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados
```bash
# Usando Docker
docker-compose up -d

# Ou configure PostgreSQL manualmente
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Execute as migrações
```bash
flask db upgrade
```

### 6. Inicie a aplicação
```bash
python run.py
```

A API estará disponível em `http://localhost:5000`

## 📊 Modelos de Dados

### Treinamento
```python
{
    "id": 1,
    "nome_treinamento": "Python Básico",
    "vendor": "TechCorp",
    "instrutor_sugerido": "João Silva"
}
```

### Turma
```python
{
    "id": 1,
    "treinamento_id": 1,
    "data_inicio": "2024-06-15",
    "horario": "09:00 - 17:00",
    "local": "Sala 1",
    "status": "Agendada"
}
```

### Aluno
```python
{
    "id": 1,
    "nome": "Maria Santos",
    "email": "maria@email.com",
    "turma_id": 1,
    "pago": false
}
```

## 🔌 Endpoints da API

### Treinamentos (Catálogo)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/treinamentos` | Lista todos os treinamentos |
| POST | `/treinamentos` | Cria novo treinamento |
| DELETE | `/treinamentos` | Remove treinamento |
| GET | `/treinamentos/<vendor>` | Busca por vendor |
| GET | `/treinamentos/instrutor/<nome>` | Busca por instrutor |

### Turmas (Agendamentos)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/treinamentos/agendados` | Lista turmas agendadas |
| POST | `/treinamentos/agendados` | Agenda nova turma |
| PUT | `/treinamentos/agendados/<id>` | Atualiza turma |

### Alunos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/alunos/` | Lista todos os alunos |
| POST | `/alunos/` | Inscreve novo aluno |

## 📝 Exemplos de Uso

### Criar Treinamento
```bash
curl -X POST http://localhost:5000/treinamentos \
  -H "Content-Type: application/json" \
  -d '{
    "nome_treinamento": "Docker Fundamentals",
    "vendor": "Docker Inc",
    "instrutor_sugerido": "Ana Silva"
  }'
```

### Agendar Turma
```bash
curl -X POST http://localhost:5000/treinamentos/agendados \
  -H "Content-Type: application/json" \
  -d '{
    "treinamento_id": 1,
    "data_inicio": "2024-08-15",
    "horario": "09:00 - 17:00",
    "local": "Sala 2"
  }'
```

### Inscrever Aluno
```bash
curl -X POST http://localhost:5000/alunos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Pedro",
    "email": "joao@email.com",
    "treinamento_id": 1,
    "pago": true
  }'
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_models.py -v
```

## 🐳 Docker

```bash
# Subir apenas o banco
docker-compose up -d db

# Subir toda a aplicação (se configurado)
docker-compose up -d
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
# Banco de Dados
DB_USER=admin_treinamentos
DB_PASSWORD=senha_super_secreta
DB_NAME=treinamentos_db
DB_HOST=localhost

# Flask
FLASK_APP=run.py
FLASK_ENV=development
```

## 📁 Estrutura do Projeto

```
notes_project/
├── app/
│   ├── models/
│   │   ├── alunos.py
│   │   ├── treinamentos.py
│   │   └── turmas.py
│   ├── routes/
│   │   ├── alunos.py
│   │   └── treinamentos.py
│   ├── __init__.py
│   └── database.py
├── tests/
│   ├── test_models.py
│   ├── test_routes_alunos.py
│   ├── test_routes_treinamentos.py
│   └── test_integration.py
├── migrations/
├── frontend/
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para suporte, abra uma issue no repositório ou entre em contato através do email: suporte@empresa.com