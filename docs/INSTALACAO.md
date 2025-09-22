# 🚀 Guia de Instalação

## Pré-requisitos

- Python 3.8+
- PostgreSQL
- Git

## Instalação Passo a Passo

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd notes_project
```

### 2. Crie Ambiente Virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure Banco de Dados

#### Opção A: Docker (Recomendado)
```bash
docker-compose up -d db
```

#### Opção B: PostgreSQL Local
1. Instale PostgreSQL
2. Crie banco: `treinamentos_db`
3. Crie usuário: `admin_treinamentos`

### 5. Configure Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com suas configurações
```

### 6. Execute Migrações
```bash
flask db upgrade
```

### 7. Inicie a Aplicação
```bash
python run.py
```

## Verificação da Instalação

Acesse: `http://localhost:5000/treinamentos`

Deve retornar: `[]`

## Problemas Comuns

### Erro de Conexão com Banco
- Verifique se PostgreSQL está rodando
- Confirme credenciais no `.env`

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Porta 5000 em Uso
Altere a porta em `run.py`:
```python
app.run(debug=True, port=5001, host='localhost')
```