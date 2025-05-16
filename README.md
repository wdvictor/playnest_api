# Playnest API

 



## 🔧 Tecnologias

- Python 3.10+
- Django 4+
- Django REST Framework
- PostgreSQL
- Swagger



## 📁 Estrutura e Objetivo

  
A API permite:

- CRUD de clientes com detalhes pessoais.
- Registro de vendas por cliente.
- Estatísticas detalhadas de vendas.
- Autenticação via token com validade de 60 minutos.
- Documentação Swagger integrada.


## 🚀 Como rodar o projeto localmente

  

### 1. Clone o repositório

```bash
git  clone  https://github.com/seu-usuario/playnest_api.git
cd  playnest_api
```

  

### 2. Crie um ambiente virtual e ative

```bash
python  -m  venv  venv
source  venv/bin/activate  # Linux
```

### 3. Instale as dependências


```bash
pip  install  -r  requirements.txt
```

 
### 4. Crie o arquivo `.env` com as variáveis necessárias

Na raiz do projeto, crie um arquivo `.env` com o seguinte conteúdo:

```
API_TOKEN=seu_token_de_api
SECRET_KEY=sua_django_secret_key
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=host
DB_PORT=port
```

> ⚠️ Certifique-se de que o PostgreSQL esteja rodando localmente com essas credenciais ou use um banco remoto (ex: Render).


### 🔄 Usando SQLite localmente (opcional)
**Altere o `settings.py`**

Substitua a configuração `DATABASES` por:
  ```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
>⚠️ **Importante:** com SQLite, o Django cria um arquivo `db.sqlite3` automaticamente no diretório raiz do projeto.

### 5. Execute as migrações

  

```bash
python  manage.py  migrate
```

### 6. Rode o servidor local


```bash
python  manage.py  runserver
```

  



  

## 🔐 Autenticação

  

Todos os endpoints da API exigem **Token de acesso**.


### Para obter o token:

#### Registro de novo usuário:

```
[POST] /api/register/
```

Payload:

```json

{
	"email": "usuario@example.com",
	"password": "sua_senha",
	"name": "Nome do Usuário",
	"birthday": "1990-01-01"
}
```

  

#### Login de usuário:

  

```

POST /api/login/

```

Payload:

```json
{
	"email": "usuario@example.com",
	"password": "sua_senha"
}
```
 
Use esse token nos headers:

```

Authorization: Bearer <token>

```

  

> O token expira em 60 minutos.

  

---

  

## 📄 Documentação da API

  

Acesse via Swagger:

  

```

GET /api/docs/

```

  

---

  

## ✅ Testes

  

Rode os testes automatizados com:

  

```bash

python  manage.py  test

```

  

---

  

## 🛑 Importante

  

- O arquivo `.env`  **NÃO deve ser versionado**.

- Adicione no `.gitignore`:

  

```

__pycache__/

*.pyc

*.sqlite3

.env

```

  

- Todas as requisições protegidas exigem token.

  

---

  

## 📬 Contato

  

Em caso de dúvidas ou sugestões, abra uma *issue* neste repositório.