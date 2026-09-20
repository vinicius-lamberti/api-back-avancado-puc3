# API Back Avançado PUC3

API REST desenvolvida em FastAPI para um e-commerce com funcionalidades de catálogo de produtos, usuários, carrinhos, listas de desejos e pedidos. A aplicação integra dados da FakeStoreAPI e também persiste dados locais de pedidos e listas de desejos em SQLite.

---

## 🚀 Visão geral

Esta API foi construída para servir como backend do projeto de interface web, permitindo:

- consulta e manipulação de produtos;
- cadastro e atualização de usuários;
- gerenciamento de carrinhos de compra;
- criação de listas de desejos;
- registro e consulta de pedidos;
- documentação automática via Swagger/OpenAPI.

A aplicação expõe a documentação interativa em:

- http://localhost:8000/docs

---

## 🧰 Requisitos

Antes de iniciar, certifique-se de que o ambiente local atende aos seguintes requisitos:

- Python 3.11+
- pip
- Git
- Docker e Docker Compose (opcional, para execução em containers)
- Acesso à internet para consumir a API externa FakeStoreAPI

---

## 📦 Clonando os repositórios

Os repositórios da API e da interface devem ficar em pastas paralelas, por exemplo:

```bash
cd ~/github

git clone https://github.com/vinicius-lamberti/interface-back-avancado-puc3.git
git clone https://github.com/vinicius-lamberti/api-back-avancado-puc3.git
```

Em seguida, entre na pasta da API:

```bash
cd api-back-avancado-puc3
```

---

## ⚙️ Configuração do ambiente local

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar a variável de ambiente do banco

O projeto usa SQLite por padrão. O valor padrão já está definido em `app/database/connection.py`:

```bash
export DATABASE_URL="sqlite:///./app.db"
```

Se quiser manter a persistência em um arquivo no diretório do projeto, essa variável é suficiente.

---

## ▶️ Iniciando a API localmente

A partir da raiz do projeto, execute:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:

- http://localhost:8000
- http://localhost:8000/docs

---

## 🐳 Executando com Docker

Também é possível executar a API em container.

### Build da imagem

```bash
docker build -t api-back-avancado-puc3 .
```

### Rodar o container

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL="sqlite:////app/data/app.db" \
  -v api_data:/app/data \
  api-back-avancado-puc3
```

Essa configuração mantém os dados do banco em um volume Docker persistente.

---

## 🧩 Executando o projeto completo

Com o ambiente pronto, a forma recomendada de subir a stack completa é no repositório da interface:

```bash
cd ~/github/interface-back-avancado-puc3
sudo docker-compose up --build
```

Após o comando, acesse:

- Documentação da API: http://localhost:8000/docs
- Aplicação frontend: http://localhost/

> Observação: o frontend e a API devem estar no mesmo ambiente Docker Compose para que a comunicação entre os serviços funcione corretamente.

---

## 🗂️ Estrutura principal do projeto

```text
api-back-avancado-puc3/
├── app/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── main.py
├── tests/
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

Principais módulos:

- `app/main.py`: configuração da aplicação FastAPI e documentação OpenAPI;
- `app/routers/`: endpoints da API por domínio (produtos, usuários, carrinhos, pedidos, wishlists, auth);
- `app/models/`: modelos ORM do banco;
- `app/schemas/`: validação e serialização de dados;
- `app/database/`: conexão e sessão com o SQLite.

---

## 🌐 API externa utilizada

A API principal do projeto integra a seguinte API externa:

- Nome: FakeStoreAPI
- Site: https://fakestoreapi.com
- Finalidade: dados de demonstração para e-commerce
- Licença: a FakeStoreAPI é uma API pública de demonstração; consulte os termos oficiais do serviço antes de uso em produção.
- Cadastro: normalmente não é necessário para uso público de leitura em ambiente de prototipagem.

### Rotas principais consumidas pela API local

- `GET /products`
- `GET /products/{product_id}`
- `GET /users/{user_id}`
- `POST /users`
- `PUT /users/{user_id}`
- `GET /carts`
- `GET /carts/{id}`

Além disso, esta API expande o uso com recursos personalizados:

- `POST /orders`
- `GET /orders/user/{user_id}`
- `GET /orders/{order_id}`
- `GET /wishlists/{user_id}`
- `POST /wishlists`
- `DELETE /wishlists/{wishlist_id}`

---

## ✅ Testes

Para executar os testes automatizados da API:

```bash
pytest
```

Ou, em modo mais enxuto:

```bash
pytest -q
```

---

## 📌 Observações importantes

- A API expõe documentação automática via Swagger em `/docs`.
- O banco local é SQLite.
- O backend pode ser usado sozinho para testes locais, mas o fluxo completo do projeto normalmente é executado junto com a interface frontend via Docker Compose.
