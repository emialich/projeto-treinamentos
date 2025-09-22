# 🏗️ Arquitetura do Sistema

## Visão Geral

Sistema de gerenciamento de treinamentos baseado em Flask com arquitetura em camadas.

## Estrutura do Projeto

```
notes_project/
├── app/                    # Aplicação principal
│   ├── models/            # Modelos de dados
│   ├── routes/            # Rotas da API
│   ├── services/          # Lógica de negócio
│   ├── utils/             # Utilitários
│   ├── __init__.py        # Factory da aplicação
│   └── database.py        # Configuração do banco
├── tests/                 # Testes automatizados
├── migrations/            # Migrações do banco
├── frontend/              # Interface web
└── docs/                  # Documentação
```

## Camadas da Aplicação

### 1. Camada de Dados (Models)
- **Treinamento**: Catálogo de cursos
- **Turma**: Agendamentos específicos
- **Aluno**: Participantes das turmas

### 2. Camada de Rotas (Routes)
- **Blueprint Treinamentos**: Endpoints do catálogo e turmas
- **Blueprint Alunos**: Endpoints de gestão de alunos

### 3. Camada de Serviços (Services)
- Lógica de negócio
- Validações complexas
- Integrações externas

## Relacionamentos

```
Treinamento (1) ──── (N) Turma (1) ──── (N) Aluno
```

- Um treinamento pode ter várias turmas
- Uma turma pertence a um treinamento
- Uma turma pode ter vários alunos
- Um aluno pertence a uma turma

## Tecnologias

### Backend
- **Flask**: Framework web
- **SQLAlchemy**: ORM
- **Flask-Migrate**: Migrações
- **PostgreSQL**: Banco de dados

### Testes
- **Pytest**: Framework de testes
- **SQLite**: Banco em memória para testes

### Infraestrutura
- **Docker**: Containerização
- **Docker Compose**: Orquestração

## Padrões Utilizados

### Factory Pattern
Aplicação criada via factory function em `app/__init__.py`

### Blueprint Pattern
Rotas organizadas em blueprints modulares

### Repository Pattern
Modelos encapsulam acesso aos dados

## Fluxo de Dados

1. **Requisição HTTP** → Routes
2. **Routes** → Services (validações)
3. **Services** → Models (persistência)
4. **Models** → Database
5. **Response JSON** ← Routes

## Configuração

### Variáveis de Ambiente
- `DATABASE_URL`: String de conexão
- `FLASK_ENV`: Ambiente (development/production)
- `FLASK_APP`: Arquivo principal

### Migrações
```bash
flask db init      # Inicializar
flask db migrate   # Criar migração
flask db upgrade   # Aplicar migração
```

## Segurança

### Implementado
- Validação de entrada
- Sanitização de dados
- Tratamento de erros

### A Implementar
- Autenticação JWT
- Rate limiting
- CORS configurado
- Logs de auditoria