# 💀 DeadOrAlive

**DeadOrAlive** é uma aplicação de monitoramento de URLs desenvolvida com FastAPI, Celery e Docker. Ela permite cadastrar URLs e verifica periodicamente sua disponibilidade, registrando o status de cada uma.

---

## 📋 Índice

- [🧰 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [⚙️ Funcionalidades](#️-funcionalidades)
- [📦 Instalação](#-instalação)
- [🛠️ Como Usar](#️-como-usar)

---

## 🧰 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [httpx](https://www.python-httpx.org/)

---

## ⚙️ Funcionalidades

- ✅ Cadastro de URLs para monitoramento.
- 🔄 Verificação periódica da disponibilidade das URLs.
- 🧾 Registro do status HTTP de cada URL.
- 🧩 Interface de API para gerenciamento das URLs monitoradas.

---

## 📦 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/jfromjefferson/dead-or-alive.git
   cd dead-or-alive
   ```
2. **Crie um <code>.env</code> na raíz do projeto com as variáveis de ambiente necessárias:**
  ```bash
  # Exemplo de conteúdo do .env
  REDIS_BROKER=redis://redis:6379/0
  REDIS_BACKEND=redis://redis:6379/0
  DATABASE_URL=sqlite:///./database.db
  ```
3. **Crie o arquivo de banco de dados**
  ```bash
  touch database.db
  ```
4. **Rode as migrações com Alembic:**
  ```bash
  alembic upgrade head
  ```
5. **Construa e inicie os containers com Docker Compose:**
  ```bash
  docker-compose up --build
  ```
A aplicação estará disponível em http://localhost:8000

---

## 🛠️ Como Usar
- Acesse a documentação interativa da API:

  Visite http://localhost:8000/docs para explorar e testar os endpoints disponíveis.

- ### Endpoints principais:

  - GET /urls
  - POST /urls
  - PATCH /urls/{id}
