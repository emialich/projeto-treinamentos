# 📖 Documentação da API

## Base URL
```
http://localhost:5000
```

## Autenticação
Atualmente a API não requer autenticação.

---

## 🎓 Treinamentos (Catálogo)

### Listar Treinamentos
```http
GET /treinamentos
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nome_treinamento": "Python Básico",
    "vendor": "TechCorp",
    "instrutor_sugerido": "João Silva"
  }
]
```

### Criar Treinamento
```http
POST /treinamentos
Content-Type: application/json

{
  "nome_treinamento": "Docker Fundamentals",
  "vendor": "Docker Inc",
  "instrutor_sugerido": "Ana Silva"
}
```

**Resposta (201):**
```json
{
  "id": 2,
  "nome_treinamento": "Docker Fundamentals",
  "vendor": "Docker Inc",
  "instrutor_sugerido": "Ana Silva"
}
```

### Buscar por Vendor
```http
GET /treinamentos/{vendor}
```

### Buscar por Instrutor
```http
GET /treinamentos/instrutor/{nome_instrutor}
```

### Remover Treinamento
```http
DELETE /treinamentos
Content-Type: application/json

{
  "id": 1,
  "nome_treinamento": "Python Básico"
}
```

---

## 📅 Turmas (Agendamentos)

### Listar Turmas Agendadas
```http
GET /treinamentos/agendados
```

### Agendar Nova Turma
```http
POST /treinamentos/agendados
Content-Type: application/json

{
  "treinamento_id": 1,
  "data_inicio": "2024-08-15",
  "horario": "09:00 - 17:00",
  "local": "Sala 2",
  "status": "Agendada"
}
```

### Atualizar Turma
```http
PUT /treinamentos/agendados/{turma_id}
Content-Type: application/json

{
  "status": "Em andamento",
  "local": "Sala 3"
}
```

---

## 👨🎓 Alunos

### Listar Alunos
```http
GET /alunos/
```

### Inscrever Aluno
```http
POST /alunos/
Content-Type: application/json

{
  "nome": "João Pedro",
  "email": "joao@email.com",
  "treinamento_id": 1,
  "pago": true
}
```

---

## ❌ Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 400 | Bad Request - Dados inválidos ou ausentes |
| 404 | Not Found - Recurso não encontrado |
| 409 | Conflict - Conflito de dados |
| 500 | Internal Server Error - Erro interno |