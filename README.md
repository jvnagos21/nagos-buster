# 🎬 Nagos - Buster

API REST para um serviço de **catálogo e compra de filmes**, construída com **Django** e **Django REST Framework**. Usuários se cadastram, fazem login com **JWT**, navegam pelo catálogo e compram filmes. Funcionários gerenciam o catálogo. 🍿

> 📚 Projeto de back-end desenvolvido durante o curso da **Kenzie Academy Brasil** (antigo *Kenzie Buster*).

---

## 📑 Sumário

- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias](#️-tecnologias)
- [🗂️ Estrutura do projeto](#️-estrutura-do-projeto)
- [🧩 Modelos de dados](#-modelos-de-dados)
- [🚀 Como rodar o projeto](#-como-rodar-o-projeto)
- [🔌 Endpoints](#-endpoints)
- [📨 Exemplos de requisições](#-exemplos-de-requisições)
- [🔐 Autenticação e permissões](#-autenticação-e-permissões)
- [🧪 Testes](#-testes)
- [👨‍💻 Autor](#-autor)

---

## ✨ Funcionalidades

- 👤 Cadastro de usuários (clientes e funcionários)
- 🔑 Login com tokens **JWT** (access e refresh)
- 🙋 Consulta e edição de perfil (somente o próprio usuário ou um funcionário)
- 🎞️ Cadastro, listagem (paginada), consulta e exclusão de filmes
- 🛒 Compra de filmes, com registro de preço e data da compra
- 🛡️ Controle de acesso: o catálogo é público para leitura e restrito a funcionários para escrita
- ✅ Suíte de testes automatizados dividida por tarefas

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| 🐍 Python | Linguagem |
| 🌿 Django 4.2 | Framework web |
| 🔧 Django REST Framework 3.14 | Construção da API |
| 🎟️ SimpleJWT 5.2 | Autenticação com JWT |
| 🗃️ SQLite | Banco de dados |
| 🧪 Pytest, pytest-django e pytest-testdox | Testes |
| ⚫ Black | Formatação de código |

---

## 🗂️ Estrutura do projeto

```
nagos-buster/
├── _core/            # ⚙️ Configurações do projeto (settings, urls, wsgi/asgi)
├── users/            # 👤 App de usuários (model, serializers, views, permissões)
├── movies/           # 🎞️ App de filmes e pedidos (model, serializers, views, permissões)
├── tests/            # 🧪 Testes e factories, organizados por tarefa (t1 a t4)
├── manage.py
├── pytest.ini
└── requirements.txt
```

---

## 🧩 Modelos de dados

### 👤 User

Estende o `AbstractUser` do Django.

| Campo | Tipo | Observações |
|---|---|---|
| `email` | EmailField | Único, até 127 caracteres |
| `username` | CharField | Único, até 150 caracteres |
| `first_name` / `last_name` | CharField | Até 50 caracteres |
| `birthdate` | DateField | Opcional |
| `is_employee` | Boolean | Padrão `false`. Se `true`, o usuário é criado com permissões de funcionário (`is_staff` e `is_superuser`) |

### 🎞️ Movie

| Campo | Tipo | Observações |
|---|---|---|
| `title` | CharField | Obrigatório, até 127 caracteres |
| `duration` | CharField | Opcional, até 10 caracteres (ex.: `120m`) |
| `rating` | Choice | `G`, `PG`, `PG-13`, `R` ou `NC-17` (padrão `G`) |
| `synopsis` | TextField | Opcional |
| `user` | ForeignKey | Funcionário que cadastrou o filme |

### 🛒 MovieOrder

| Campo | Tipo | Observações |
|---|---|---|
| `movie` | ForeignKey | Filme comprado |
| `user` | ForeignKey | Usuário que comprou |
| `price` | Decimal | Até 8 dígitos, 2 casas decimais |
| `buyed_at` | DateTime | Preenchido automaticamente |

---

## 🚀 Como rodar o projeto

### 📋 Pré-requisitos

- Python 3.10 ou superior
- `pip` e `venv`
- Git

### 🔽 Passo a passo

1. **Clone o repositório** 📥
   ```bash
   git clone https://github.com/jvnagos21/nagos-buster.git
   cd nagos-buster
   ```

2. **Crie e ative o ambiente virtual** 🌱
   ```bash
   python -m venv venv

   # Linux / macOS
   source venv/bin/activate

   # Windows (PowerShell)
   .\venv\Scripts\activate

   # Windows (Git Bash)
   source venv/Scripts/activate
   ```

3. **Instale as dependências** 📦
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações** 🗄️
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor** ▶️
   ```bash
   python manage.py runserver
   ```

A API ficará disponível em `http://127.0.0.1:8000/api/` 🎉

---

## 🔌 Endpoints

Todas as rotas têm o prefixo `/api/`.

### 👤 Usuários

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| `POST` | `/users/` | Cadastra um usuário | 🌍 Público |
| `POST` | `/users/login/` | Gera os tokens JWT | 🌍 Público |
| `GET` | `/users/<id>/` | Consulta um usuário | 🔒 Próprio usuário ou funcionário |
| `PATCH` | `/users/<id>/` | Atualiza um usuário | 🔒 Próprio usuário ou funcionário |

### 🎞️ Filmes

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| `GET` | `/movies/` | Lista os filmes (paginado) | 🌍 Público |
| `POST` | `/movies/` | Cadastra um filme | 🛡️ Funcionário |
| `GET` | `/movies/<id>/` | Consulta um filme | 🌍 Público |
| `DELETE` | `/movies/<id>/` | Remove um filme | 🛡️ Funcionário |

### 🛒 Pedidos

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| `POST` | `/movies/<id>/orders/` | Compra um filme | 🔒 Usuário autenticado |

> 📄 A listagem de filmes é paginada, com **2 itens por página**. Use `?page=2` para navegar.

---

## 📨 Exemplos de requisições

### 👤 Cadastrar usuário

`POST /api/users/`

```json
{
  "username": "joao",
  "email": "joao@mail.com",
  "password": "1234",
  "first_name": "João",
  "last_name": "Vitor",
  "birthdate": "1998-05-20",
  "is_employee": true
}
```

**Resposta `201 Created`** (a senha nunca é retornada 🙈)

```json
{
  "id": 1,
  "email": "joao@mail.com",
  "username": "joao",
  "first_name": "João",
  "last_name": "Vitor",
  "birthdate": "1998-05-20",
  "is_employee": true,
  "is_superuser": true
}
```

### 🔑 Fazer login

`POST /api/users/login/`

```json
{
  "username": "joao",
  "password": "1234"
}
```

**Resposta `200 OK`**

```json
{
  "refresh": "<token_refresh>",
  "access": "<token_access>"
}
```

Nas rotas protegidas, envie o token no cabeçalho:

```
Authorization: Bearer <token_access>
```

### 🎞️ Cadastrar filme (funcionário)

`POST /api/movies/`

```json
{
  "title": "Interestelar",
  "duration": "169m",
  "rating": "PG-13",
  "synopsis": "Um grupo de astronautas viaja através de um buraco de minhoca."
}
```

**Resposta `201 Created`**

```json
{
  "id": 1,
  "title": "Interestelar",
  "synopsis": "Um grupo de astronautas viaja através de um buraco de minhoca.",
  "rating": "PG-13",
  "duration": "169m",
  "added_by": "joao@mail.com"
}
```

### 🛒 Comprar filme

`POST /api/movies/1/orders/`

```json
{
  "price": 29.90
}
```

**Resposta `201 Created`**

```json
{
  "id": 1,
  "title": "Interestelar",
  "price": "29.90",
  "buyed_by": "joao@mail.com",
  "buyed_at": "2026-10-17T01:40:00.000000Z"
}
```

---

## 🔐 Autenticação e permissões

| Perfil | O que pode fazer |
|---|---|
| 🌍 **Visitante** | Cadastrar-se, fazer login, listar e consultar filmes |
| 🙋 **Usuário autenticado** | Tudo do visitante, mais consultar e editar o próprio perfil e comprar filmes |
| 🛡️ **Funcionário** | Tudo do usuário, mais cadastrar e remover filmes e consultar e editar qualquer usuário |

- ⏱️ O token de acesso expira em **120 minutos**.
- 🚫 Sem permissão, a API responde `403 Forbidden`. Sem token válido, `401 Unauthorized`.

---

## 🧪 Testes

Os testes usam **pytest** com **pytest-django** e **pytest-testdox**, e já vêm configurados em `pytest.ini`.

> ⚠️ Se você tiver `pytest`, `pytest-testdox` ou `pytest-django` instalados **globalmente**, desinstale-os e use apenas o ambiente virtual do projeto, para evitar conflitos de versão.

Com o ambiente virtual ativado, rode todos os testes:

```bash
pytest --testdox -vvs
```

Ou rode os testes de cada tarefa isoladamente:

| Tarefa | Comando |
|---|---|
| 1️⃣ Tarefa 1 | `pytest --testdox -vvs tests/tarefas/t1/` |
| 2️⃣ Tarefa 2 | `pytest --testdox -vvs tests/tarefas/t2/` |
| 3️⃣ Tarefa 3 | `pytest --testdox -vvs tests/tarefas/t3/` |
| 4️⃣ Tarefa 4 | `pytest --testdox -vvs tests/tarefas/t4/` |

---

## 👨‍💻 Autor

Feito com 💜 por **João Vitor Meira Vieira**

- 🐙 GitHub: [@jvnagos21](https://github.com/jvnagos21)

⭐ Se este projeto te ajudou, deixe uma estrela no repositório!
