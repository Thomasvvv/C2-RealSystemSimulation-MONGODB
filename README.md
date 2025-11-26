# 🎓 Sistema de Gestão de Estudantes

Sistema de gerenciamento acadêmico desenvolvido para fins educacionais na disciplina de Banco de Dados (Prof. Howard).

O sistema permite realizar operações CRUD completas para alunos, cursos, professores, matérias, ofertas e matrículas, além de gerar relatórios dinâmicos e dashboards de desempenho.

---

## 🧭 Visão Geral

O projeto é dividido em duas camadas principais:

- **Backend:** Desenvolvido em Python (Flask) com **MongoDB**
- **Frontend:** Desenvolvido em HTML, CSS e JavaScript, com painéis dinâmicos e modais interativos

---

## 📁 Estrutura do Projeto

```
C2-RealSystemSimulation-OracleDataBase/
├── backend/
│   ├── controllers/          # Controladores para cada entidade
│   ├── db/                   # Configuração e conexão com MongoDB
│   ├── app.py                # Aplicação Flask principal
│   ├── requirements.txt      # Dependências Python
│   └── .env.example          # Exemplo de configuração
├── frontend/
│   ├── index.html            # Interface principal
│   ├── scripts/              # JavaScript (API, CRUD, relatórios)
│   └── styles/               # CSS global
├── DataBase/
│   └── Create_Collections.js # Script de criação das coleções
└── README.md
```

---

## ⚙️ Instalação e Configuração

### 1. 🧩 Requisitos

- **Python 3.x**
- **MongoDB Community Server**
- **pip**

---

### 2. 📦 Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

---

### 3. 🔐 Configurar Variáveis de Ambiente

Crie o arquivo `.env` baseado em `.env.example`:

```ini
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=student_system
```

---

### 4. 🗃️ Criar o Banco de Dados (MongoDB)

Crie as coleções executando o arquivo de inicialização:

```
DataBase/Create_Collections.js
```

Exemplo de criação das coleções:

```javascript
db.createCollection("students")
db.createCollection("courses")
db.createCollection("teachers")
db.createCollection("subjects")
db.createCollection("offers")
db.createCollection("enrollments")
```

---

## 5. 🚀 Executar o Backend

```bash
cd backend
python app.py
```

A aplicação iniciará em:

```
http://localhost:5000
```

### Exemplos de endpoints:

```bash
GET http://localhost:5000/api/students
POST http://localhost:5000/api/students
GET http://localhost:5000/api/reports/course-statistics
```

---

## 6. 🌐 Acessar o Frontend

Abra:

```
frontend/index.html
```

**Funcionalidades disponíveis:**

- 📋 CRUD completo  
- 🔄 Edição inline  
- 📊 Relatórios dinâmicos  
- 🎯 Dashboard em tempo real  

---

## 🧱 Funcionalidades Principais

### 🧍‍♂️ Alunos
- CRUD completo
- Validação de dados
- Suporte a múltiplos formatos de data

### 🎓 Cursos
- Cadastro e manutenção de cursos
- Associação com matérias e alunos
- Controle de carga horária

### 👩‍🏫 Professores
- Registro e gerenciamento
- Consultas por oferta
- Status ativo/inativo

### 📚 Matérias e Ofertas
- Associação de matérias a cursos
- Professores responsáveis
- Controle de períodos letivos

### 📝 Matrículas
- Status do aluno
- Integração com ofertas
- Validações de integridade

---

# 📊 Relatórios (MongoDB)

### ▶️ Estatísticas por Curso

```javascript
db.students.aggregate([
  { 
    $group: { 
      _id: "$course_id", 
      total: { $sum: 1 } 
    } 
  }
])
```

### ▶️ Ofertas Completas

```javascript
db.offers.aggregate([
  {
    $lookup: {
      from: "subjects",
      localField: "subject_id",
      foreignField: "_id",
      as: "subject"
    }
  },
  {
    $lookup: {
      from: "teachers",
      localField: "teacher_id",
      foreignField: "_id",
      as: "teacher"
    }
  }
])
```

### ▶️ Dashboard Geral

```javascript
db.students.countDocuments()
db.courses.countDocuments()
db.offers.countDocuments()
```

---

## 🧰 Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask 2.3.2
- PyMongo 4.6.1
- Flask-CORS 4.0.0
- python-dotenv 1.0.0

### Frontend
- HTML5
- CSS3
- JavaScript Vanilla
- Fetch API

### Banco de Dados
- MongoDB Community Server
- Coleções relacionais via Modelagem NoSQL
- Agregações (aggregate pipeline)

---

## 🧩 Características Técnicas

- Arquitetura modularizada
- Endpoints RESTful
- Validação de dados
- Conexão via PyMongo
- Agregações avançadas
- Logs e tratamento de erros
- Dashboard em tempo real

---

## 🔧 Troubleshooting

### ❌ Erro: MongoDB não encontrado
- Verifique se o serviço está rodando:
```bash
sudo systemctl start mongod
```
ou
```bash
mongod
```

### ❌ Erro de conexão no backend
- Verifique o arquivo `.env`
- Confirme a porta `27017`

### ❌ Frontend não conecta
- Verifique se o backend está rodando
- Limpe cache do navegador (Ctrl+Shift+R)

---

## 👥 Equipe de Desenvolvimento

- Bernardo Lodi  
- João Guilherme  
- Luanna Moreira  
- Luiz Hélio  
- Pedro Sousa  
- Thomas Veiga  

---

## 📘 Licença

Este projeto está sob a licença MIT.

---

© 2025 — Sistema de Gestão de Estudantes.



