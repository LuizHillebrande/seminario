# Seminário - Arquitetura de Microserviços

## 📋 Visão Geral

Projeto educacional implementando uma arquitetura de **microserviços** com dois serviços independentes:
- **Auth Service**: Autenticação, cadastro e validação de usuários
- **User Service**: Gerenciamento de perfil de usuário

Cada serviço roda em uma porta diferente, tem seu próprio banco de dados SQLite e se comunica via HTTP/JWT.

---

## 🏗️ Arquitetura

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    Cliente (Navegador)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
   ┌────▼─────────┐              ┌───────▼──────┐
   │ Auth Service │              │ User Service │
   │  (5000)      │              │   (5002)     │
   └────┬─────────┘              └───────▲──────┘
        │                              │
        │ Redirecionamento com JWT     │
        └──────────────────────────────┘
```

### Serviços

#### **Auth Service** (Porto 5000)
- **Banco de dados**: `auth_service/auth.db` (SQLite)
- **Responsabilidades**:
  - Cadastro de usuários
  - Validação de contas
  - Login com geração de JWT
- **Endpoints**:
  ```
  GET  /                     → Página inicial (cadastro/login)
  GET  /health               → Status do serviço
  GET  /api-info             → Documentação dos endpoints
  POST /auth/register        → Cadastro de novo usuário
  GET  /validate?user_id=X   → Página de validação
  POST /validate             → Confirmar validação
  POST /auth/login           → Login (retorna JWT)
  ```

#### **User Service** (Porto 5002)
- **Banco de dados**: `user_service/user.db` (SQLite)
- **Responsabilidades**:
  - Exibir perfil do usuário autenticado
  - Validar e processar tokens JWT
- **Endpoints**:
  ```
  GET  /                     → Página de perfil (com token JWT)
  GET  /health               → Status do serviço
  ```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou navegue para o projeto**:
   ```bash
   cd C:\Users\User\OneDrive\Documentos\Seminario\seminario
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

### Rodando os Serviços

Abra **dois terminais** separados na pasta `seminario`:

**Terminal 1 - Auth Service**:
```bash
python auth_service/app.py
```
Acesse: http://localhost:5000/

**Terminal 2 - User Service**:
```bash
python user_service/app.py
```
Acesse (após login): http://localhost:5002/

---

## 📊 Fluxo de Uso

### 1. **Cadastro**
- Acesse http://localhost:5000/
- Preencha: **email**, **nome** e **senha**
- Clique **"Registrar"**
- O sistema cria o usuário e redireciona para validação

### 2. **Validação**
- Na página `/validate`, clique **"Validar Conta"**
- Mensagem de sucesso aparece
- Sua conta agora está pronta para login

### 3. **Login**
- Volte à página inicial (http://localhost:5000/)
- Mude para a seção **"Login"** (clique no link)
- Insira **email** e **senha**
- Clique **"Entrar"**
- Você será redirecionado para http://localhost:5002/?token=JWT
- A página exibe seu token JWT

### 4. **Perfil de Usuário**
- No User Service, você vê a mensagem de sucesso e seu token
- Clique **"Mostrar token completo"** para visualizar o JWT decodificado

---

## 🔐 Segurança

### JWT (JSON Web Token)

O token JWT contém:
- **Tipo**: Bearer
- **Payload**:
  - `sub` (subject): ID do usuário
  - `email`: Email do usuário
  - `exp` (expiration): Data de expiração
- **Assinatura**: Válida apenas com a chave secreta definida em `.env`

### Variáveis de Ambiente

Arquivo `.env` na pasta `seminario/`:
```env
SECRET_KEY=supersecret
JWT_SECRET_KEY=jwt-secret-change-in-production
DATABASE_URL=sqlite:///auth.db
USER_DATABASE_URL=sqlite:///user.db
```

**⚠️ Em produção, altere estas chaves!**

---

## 📁 Estrutura do Projeto

```
seminario/
├── .env                          # Variáveis de ambiente
├── requirements.txt              # Dependências Python
├── auth_service/
│   ├── app.py                   # Aplicação Flask
│   ├── config.py                # Configuração
│   ├── extensions.py            # Extensões (DB, JWT)
│   ├── models.py                # Modelo de usuário
│   ├── routes.py                # Rotas de autenticação
│   ├── auth.db                  # Banco de dados SQLite
│   └── templates/
│       ├── index.html           # Página de cadastro/login
│       ├── validate.html        # Página de validação
│       └── success.html         # Página de sucesso
│
├── user_service/
│   ├── app.py                   # Aplicação Flask
│   ├── config.py                # Configuração
│   ├── extensions.py            # Extensões (DB, JWT)
│   ├── models.py                # Modelo de perfil
│   ├── routes.py                # Rotas de perfil
│   ├── user.db                  # Banco de dados SQLite
│   └── templates/
│       └── index.html           # Página de perfil
│
└── instance/                     # Pasta de cache SQLAlchemy
```

---

## 🔌 Endpoints da API

### Auth Service

#### Cadastro
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "usuario@example.com",
  "name": "João Silva",
  "password": "senha123"
}

Resposta: Redirecionamento para /validate?user_id=1
```

#### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "senha123"
}

Resposta (JSON):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Resposta (Formulário HTML):
Redirecionamento para http://localhost:5002/?token=JWT
```

#### Health Check
```bash
GET /health

Resposta:
{
  "service": "auth",
  "status": "ok"
}
```

### User Service

#### Perfil com Token
```bash
GET /?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Resposta: Página HTML com informações do token
```

#### Health Check
```bash
GET /health

Resposta:
{
  "service": "user",
  "status": "ok"
}
```

---

## 🛠️ Tecnologias Utilizadas

- **Framework**: Flask (Python)
- **Autenticação**: Flask-JWT-Extended
- **Banco de Dados**: SQLAlchemy + SQLite
- **Segurança**: Werkzeug (hash de senha)
- **Templates**: Jinja2

---

## 📝 Configuração de Banco de Dados

### Auto-recriação (Desenvolvimento)

Os arquivos `app.py` de ambos os serviços contêm lógica para recriar o banco automaticamente:

```python
with app.app_context():
    db.drop_all()      # Remove todas as tabelas
    db.create_all()    # Recria com schema atual
```

**Isso garante sincronização entre modelo e schema em desenvolvimento.**

---

## 🐛 Troubleshooting

### Erro: "no such column: user.name"
- **Causa**: Schema do banco desatualizado
- **Solução**: Bancos são recriados automaticamente ao iniciar os serviços

### Erro: "TemplateNotFound"
- **Causa**: Pasta `templates/` ausente
- **Solução**: Verifique se a pasta existe em cada serviço

### Erro: "CONNECTION REFUSED (localhost:5000)"
- **Causa**: Serviço não está rodando
- **Solução**: Execute `python auth_service/app.py` em um terminal

### Token não funciona no User Service
- **Causa**: Chave JWT diferente entre serviços
- **Solução**: Verifique se a variável `JWT_SECRET_KEY` em `.env` é igual em ambos

---

## 🚀 Próximos Passos (Opcional)

### Melhorias Sugeridas

1. **API Gateway**: Centralizador de rotas
   - Roteamento inteligente
   - Rate limiting
   - Logging centralizado

2. **Email Service**: Notificações por e-mail
   - Confirmação de cadastro
   - Recuperação de senha
   - Notificações

3. **Docker**: Containerização
   - `Dockerfile` para cada serviço
   - `docker-compose.yml` para orquestração

4. **Kubernetes**: Orquestração em produção
   - Service discovery automático
   - Load balancing
   - Auto-scaling

5. **Banco de Dados Centralizado**: PostgreSQL em produção
   - Melhor escalabilidade
   - Replicação e backup

6. **Message Queue**: RabbitMQ/Redis
   - Comunicação assíncrona
   - Filas de processamento

---

## 📄 Licença

Este é um projeto educacional para fins de aprendizado.

---

## ✉️ Suporte

Para dúvidas ou sugestões sobre o projeto, consulte a documentação dos endpoints acima ou execute:

```bash
GET /api-info
```

em ambos os serviços para detalhes completos.

---

**Versão**: 1.0  
**Data**: 29 de Março de 2026  
**Status**: ✅ Em funcionamento
