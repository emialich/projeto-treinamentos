# 📝 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.0.0] - 2024-01-XX

### ✨ Adicionado
- Sistema completo de gerenciamento de treinamentos
- API REST com endpoints para treinamentos, turmas e alunos
- Modelos de dados com relacionamentos
- Sistema de migrações com Flask-Migrate
- Testes automatizados com pytest
- Documentação completa da API
- Configuração Docker para desenvolvimento
- Suporte a PostgreSQL

### 🎓 Funcionalidades
- **Catálogo de Treinamentos**
  - Criar, listar e remover treinamentos
  - Buscar por vendor e instrutor
  - Validação de integridade referencial

- **Gestão de Turmas**
  - Agendar turmas para treinamentos
  - Atualizar status e informações
  - Listar turmas futuras

- **Gestão de Alunos**
  - Inscrever alunos em turmas
  - Controle de pagamento
  - Email único por aluno

### 🏗️ Arquitetura
- Padrão Factory para criação da aplicação
- Blueprints para organização de rotas
- SQLAlchemy ORM para persistência
- Fixtures para testes isolados

### 📊 Modelos
- `Treinamento`: Catálogo de cursos disponíveis
- `Turma`: Agendamentos específicos de treinamentos
- `Aluno`: Participantes inscritos em turmas

### 🧪 Testes
- Cobertura completa dos modelos
- Testes de integração entre módulos
- Testes de API endpoints
- Banco SQLite em memória para testes

### 📚 Documentação
- README principal com guia de instalação
- Documentação detalhada da API
- Guia de arquitetura do sistema
- Guia de desenvolvimento
- Exemplos de uso com curl

---

## Formato

Este changelog segue o formato [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

### Tipos de Mudanças
- `✨ Adicionado` para novas funcionalidades
- `🔄 Alterado` para mudanças em funcionalidades existentes
- `❌ Removido` para funcionalidades removidas
- `🐛 Corrigido` para correções de bugs
- `🔒 Segurança` para vulnerabilidades corrigidas