from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.database.connection import Base, engine
from app.routers import auth, carts, orders, products, users, wishlists


@asynccontextmanager
async def lifespan(_: FastAPI):
	Base.metadata.create_all(bind=engine)
	yield


app = FastAPI(title="API Back Avançado PUC3", lifespan=lifespan)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root_redirect():
	return RedirectResponse(url="/docs")


BAD_REQUEST_DESCRIPTION = "Bad request"
SUCCESS_DESCRIPTION = "Success"
WISHLIST_NOT_FOUND_DESCRIPTION = "Wishlist not found"
APPLICATION_JSON = "application/json"


def ref(schema_name: str):
	return {"$ref": f"#/components/schemas/{schema_name}"}


def json_schema(schema_name: str):
	return {APPLICATION_JSON: {"schema": ref(schema_name)}}


def success_response(schema_name: str | None = None, description: str = SUCCESS_DESCRIPTION):
	payload = {"description": description}
	if schema_name:
		payload["content"] = json_schema(schema_name)
	return payload


FAKESTORE_OPENAPI = {
	"openapi": "3.1.0",
	"info": {
		"title": "FakeStoreAPI (Versão Estendida)",
		"description": (
			"Uma API falsa e gratuita para testes e prototipagem de aplicações de comércio eletrônico (e-commerce).\n\n"
			"### ⭐ Extensões Customizadas (Funcionalidades Extras)\n"
			"Esta versão estendida inclui recursos adicionais desenvolvidos exclusivamente para o projeto:\n"
			"* **💝 Wishlists**: Gerenciamento de listas de desejos personalizadas por usuário.\n"
			"* **🧾 Orders**: Sistema completo de finalização de compra (checkout) e histórico de pedidos de clientes."
		),
		"version": "v2.1.11-custom",
		"contact": {
			"email": "support@fakestoreapi.com",
			"url": "https://fakestoreapi.com",
		},
		"x-logo": {"url": "/icons/logo.png", "href": "/"},
	},
	"tags": [
		# Features customizadas desenvolvidas para o projeto:
		{
			"name": "Wishlists",
			"x-displayName": "💝 ⭐ Listas de Desejos [MINHA EXTENSÃO]",
			"description": "Recurso personalizado para gerenciar os produtos favoritos dos usuários."
		},
		{
			"name": "Orders",
			"x-displayName": "🧾 ⭐ Pedidos [MINHA EXTENSÃO]",
			"description": "Recurso personalizado para fechamento de compras e histórico de pedidos."
		},
		# Recursos originais da API FakeStoreAPI:
		{
			"name": "Products",
			"x-displayName": "🛒 Produtos",
			"description": "Endpoints originais para gerenciamento do catálogo de produtos."
		},
		{
			"name": "Carts",
			"x-displayName": "🛍️ Carrinhos",
			"description": "Endpoints originais para gerenciamento de carrinhos de compras temporários."
		},
		{
			"name": "Users",
			"x-displayName": "👤 Usuários",
			"description": "Endpoints originais para cadastro e perfis de usuários."
		},
		{
			"name": "Auth",
			"x-displayName": "🔒 Autenticação",
			"description": "Endpoints originais para geração de tokens de login."
		}
	],
	"servers": [
		{"url": "http://localhost:8000", "description": "Servidor de Desenvolvimento Local"}
	],
	"paths": {
		"/products": {
			"get": {
				"summary": "Obter todos os produtos",
				"description": "Retorna uma lista contendo todos os produtos disponíveis no catálogo.",
				"operationId": "getAllProducts",
				"tags": ["Products"],
				"responses": {
					"200": success_response("Product"),
					"400": {"description": BAD_REQUEST_DESCRIPTION}
				},
			},
			"post": {
				"summary": "Adicionar um novo produto",
				"description": "Cria e registra um novo produto no catálogo.",
				"operationId": "addProduct",
				"tags": ["Products"],
				"requestBody": {"required": True, "content": json_schema("Product")},
				"responses": {
					"201": {"description": "Product created successfully", "content": json_schema("Product")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}
				},
			},
		},
		"/products/{id}": {
			"get": {
				"summary": "Obter um único produto",
				"description": "Retorna os detalhes de um produto específico filtrado pelo ID.",
				"operationId": "getProductById",
				"tags": ["Products"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {
					"200": success_response("Product"),
					"400": {"description": BAD_REQUEST_DESCRIPTION},
					"404": {"description": "Produto não encontrado"}
				},
			},
			"put": {
				"summary": "Atualizar um produto",
				"description": "Atualiza as informações de um produto existente com base no ID fornecido.",
				"operationId": "updateProduct",
				"tags": ["Products"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"requestBody": {"required": True, "content": json_schema("Product")},
				"responses": {
					"200": {"description": "Product updated successfully", "content": json_schema("Product")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}
				},
			},
			"delete": {
				"summary": "Excluir um produto",
				"description": "Remove permanentemente um produto específico do catálogo usando o ID.",
				"operationId": "deleteProduct",
				"tags": ["Products"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {
					"200": {"description": "Product deleted successfully"},
					"400": {"description": BAD_REQUEST_DESCRIPTION}
				},
			},
		},
		"/carts": {
			"get": {
				"summary": "Obter todos os carrinhos",
				"description": "Retorna uma lista de todos os carrinhos de compras ativos.",
				"operationId": "getAllCarts",
				"tags": ["Carts"],
				"responses": {"200": success_response("Cart"), "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"post": {
				"summary": "Adicionar um novo carrinho",
				"description": "Cria um novo carrinho de compras para um usuário.",
				"operationId": "addCart",
				"tags": ["Carts"],
				"requestBody": {"required": True, "content": json_schema("Cart")},
				"responses": {
					"201": {"description": "Cart created successfully", "content": json_schema("Cart")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}}
				}
		},
		"/carts/{id}": {
			"get": {
				"summary": "Obter um único carrinho",
				"description": "Retorna as informações de um carrinho baseado no ID.",
				"operationId": "getCartById", "tags": ["Carts"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {
					"200": success_response("Cart"),
					"400": {"description": BAD_REQUEST_DESCRIPTION},
					"404": {"description": "Carrinho não encontrado"}
				}},
			"put": {
				"summary": "Atualizar um carrinho",
				"description": "Atualiza os itens de um carrinho existente por ID.",
				"operationId": "updateCart",
				"tags": ["Carts"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"requestBody": {"required": True, "content": json_schema("Cart")},
				"responses": {
					"200": {"description": "Cart updated successfully", "content": json_schema("Cart")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}}
				},
			"delete": {
				"summary": "Excluir um carrinho",
				"description": "Remove um carrinho de compras específico através do ID.",
				"operationId": "deleteCart", "tags": ["Carts"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {
					"200": {"description": "Cart deleted successfully"},
					"400": {"description": BAD_REQUEST_DESCRIPTION}}
				},
		},
		"/users": {
			"get": {
				"summary": "Obter todos os usuários",
				"description": "Retorna uma listagem de todos os usuários cadastrados.",
				"operationId": "getAllUsers", "tags": ["Users"],
				"responses": {"200": success_response("User"), "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"post": {
				"summary": "Adicionar um novo usuário",
				"description": "Registra e cria um novo perfil de usuário no sistema.",
				"operationId": "addUser", "tags": ["Users"],
				"requestBody": {"required": True, "content": json_schema("User")},
				"responses": {
					"201": {"description": "User created successfully","content": json_schema("User")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}}
				},
		},
		"/users/{id}": {
			"get": {
				"summary": "Obter um único usuário",
				"description": "Retorna as informações cadastrais de um usuário específico por ID.",
				"operationId": "getUserById", "tags": ["Users"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {
					"200": success_response("User"),
					"400": {"description": BAD_REQUEST_DESCRIPTION},
					"404": {"description": "Usuário não encontrado"}
					}
				},
			"put": {
				"summary": "Atualizar um usuário",
				"description": "Modifica os dados de um usuário existente com base em seu ID.",
				"operationId": "updateUser", "tags": ["Users"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"requestBody": {"required": True, "content": json_schema("User")},
				"responses": {
					"200": {"description": "User updated successfully", "content": json_schema("User")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}}
				},
			"delete": {
				"summary": "Excluir um usuário",
				"description": "Remove de forma definitiva o perfil de um usuário pelo ID.",
				"operationId": "deleteUser", "tags": ["Users"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {
					"200": {"description": "User deleted successfully"},
					"400": {"description": BAD_REQUEST_DESCRIPTION}}
				},
		},
		"/auth/login": {
			"post": {
				"summary": "Autenticação de Usuário (Login)",
				"description": "Valida as credenciais do usuário e retorna um token de acesso.",
				"operationId": "loginUser", "tags": ["Auth"],
				"requestBody": {"required": True, "content": json_schema("Login")},
				"responses": {
					"200": {"description": "Login efetuado com sucesso","content": json_schema("LoginResponse")},
					"400": {"description": BAD_REQUEST_DESCRIPTION}},
					"401": {"description": "Falha na autenticação"},
					"502": {"description": "FakeStoreAPI indisponível"}
				},
		},
		"/wishlists": {
		"post": {
			"summary": "Criar uma lista de desejos", 
			"description": "Gera uma nova lista de desejos vinculada a um usuário específico.", 
			"operationId": "createWishlist", 
			"tags": ["Wishlists"], 
			"requestBody": {"required": True, "content": json_schema("WishlistCreate")}, 
			"responses": {
				"201": {"description": "Lista de desejos criada com sucesso", "content": json_schema("Wishlist")}, 
				"400": {"description": "Usuário já possui 4 wishlists"}
			}
		},
	},
	"/wishlists/user/{user_id}": {
		"get": {
			"summary": "Listar listas de desejos por usuário", 
			"description": "Retorna todas as listas de desejos pertencentes a um usuário específico.", 
			"operationId": "listUserWishlists", 
			"tags": ["Wishlists"], 
			"parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"responses": {
				"200": {
					"description": SUCCESS_DESCRIPTION, 
					"content": {APPLICATION_JSON: {"schema": {"type": "array", "items": ref("Wishlist")}}}
				}
			}
		},
	},
	"/wishlists/{wishlist_id}": {
		"get": {
			"summary": "Obter uma lista de desejos", 
			"description": "Retorna os detalhes de uma lista de desejos específica.", 
			"operationId": "getWishlist", 
			"tags": ["Wishlists"], 
			"parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"responses": {
				"200": success_response("Wishlist"), 
				"404": {"description": "Wishlist não encontrada"}
			}
		},
		"put": {
			"summary": "Atualizar uma lista de desejos", 
			"description": "Atualiza o nome de uma lista de desejos existente.", 
			"operationId": "updateWishlist", 
			"tags": ["Wishlists"], 
			"parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"requestBody": {"required": True, "content": json_schema("WishlistUpdate")}, 
			"responses": {
				"200": success_response("Wishlist"), 
				"404": {"description": "Wishlist não encontrada"}
			}
		},
		"delete": {
			"summary": "Excluir uma lista de desejos", 
			"description": "Remove permanentemente uma lista de desejos pelo ID.", 
			"operationId": "deleteWishlist", 
			"tags": ["Wishlists"], 
			"parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"responses": {
				"204": {"description": "Lista de desejos excluída com sucesso"}, 
				"404": {"description": WISHLIST_NOT_FOUND_DESCRIPTION}
			}
		},
	},
	"/wishlists/{wishlist_id}/items": {
		"post": {
			"summary": "Adicionar item à lista de desejos", 
			"description": "Adiciona um produto específico dentro de uma lista de desejos existente.", 
			"operationId": "addWishlistItem", 
			"tags": ["Wishlists"], 
			"parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"requestBody": {"required": True, "content": json_schema("WishlistItemCreate")}, 
			"responses": {
				"201": {"description": "Item adicionado com sucesso", "content": json_schema("WishlistItem")}, 
				"400": {"description": "Produto já está na wishlist"}
			}
		},
	},
	"/wishlists/{wishlist_id}/items/{product_id}": {
		"delete": {
			"summary": "Excluir item da lista de desejos", 
			"description": "Remove um produto de dentro de uma lista de desejos.", 
			"operationId": "deleteWishlistItem", 
			"tags": ["Wishlists"], 
			"parameters": [
				{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}, 
				{"name": "product_id", "in": "path", "required": True, "schema": {"type": "integer"}}
			], 
			"responses": {
				"204": {"description": "Item excluído com sucesso"}, 
				"404": {"description": "Item não encontrado"}
			}
		},
	},
	"/orders": {
		"post": {
			"summary": "Criar um pedido", 
			"description": "Registra uma nova compra/pedido para um usuário.", 
			"operationId": "createOrder", 
			"tags": ["Orders"], 
			"requestBody": {"required": True, "content": json_schema("CreateOrderPayload")}, 
			"responses": {
				"201": {"description": "Pedido criado com sucesso", "content": json_schema("Order")}, 
				"400": {"description": "Pedido deve possuir itens"}
			}
		},
	},
	"/orders/user/{user_id}": {
		"get": {
			"summary": "Listar pedidos por usuário", 
			"description": "Retorna o histórico de pedidos realizados por um usuário específico.", 
			"operationId": "listUserOrders", 
			"tags": ["Orders"], 
			"parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"responses": {
				"200": {
					"description": SUCCESS_DESCRIPTION, 
					"content": {APPLICATION_JSON: {"schema": {"type": "array", "items": ref("Order")}}}
				}
			}
		},
	},
	"/orders/{order_id}": {
		"get": {
			"summary": "Obter detalhes de um pedido", 
			"description": "Retorna as informações detalhadas de um pedido específico utilizando o ID informado.", 
			"operationId": "getOrder", 
			"tags": ["Orders"], 
			"parameters": [{"name": "order_id", "in": "path", "required": True, "schema": {"type": "integer"}}], 
			"responses": {
				"200": success_response("Order"), 
				"404": {"description": "Pedido não encontrado"}
			}
		},
	},
	},
	"components": {
		"schemas": {
			"Product": {"type": "object", "properties": {"id": {"type": "integer"}, "title": {"type": "string"}, "price": {"type": "number", "format": "float"}, "description": {"type": "string"}, "category": {"type": "string"}, "image": {"type": "string", "format": "uri"}}},
			"Cart": {"type": "object", "properties": {"id": {"type": "integer"}, "userId": {"type": "integer"}, "products": {"type": "array", "items": ref("Product")}}},
			"User": {"type": "object", "properties": {"id": {"type": "integer"}, "username": {"type": "string"}, "email": {"type": "string"}, "password": {"type": "string"}}},
			"Login": {"type": "object", "properties": {"username": {"type": "string"}, "password": {"type": "string"}}},
			"LoginResponse": {"type": "object", "properties": {"token": {"type": "string"}}},
			"WishlistItemCreate": {"type": "object", "properties": {"product_id": {"type": "integer"}}},
			"WishlistItem": {"type": "object", "properties": {"id": {"type": "integer"}, "product_id": {"type": "integer"}, "added_at": {"type": "string", "format": "date-time"}}},
			"WishlistCreate": {"type": "object", "properties": {"user_id": {"type": "integer"}, "name": {"type": "string"}}},
			"WishlistUpdate": {"type": "object", "properties": {"name": {"type": "string"}}},
			"Wishlist": {"type": "object", "properties": {"id": {"type": "integer"}, "user_id": {"type": "integer"}, "name": {"type": "string"}, "items": {"type": "array", "items": ref("WishlistItem")}}},
			"OrderItemInput": {"type": "object", "properties": {"product_id": {"type": "integer"}, "quantity": {"type": "integer"}, "price_at_purchase": {"type": "number", "format": "float"}}},
			"CreateOrderPayload": {"type": "object", "properties": {"user_id": {"type": "integer"}, "items": {"type": "array", "items": ref("OrderItemInput")}}},
			"Order": {"type": "object", "properties": {"id": {"type": "integer"}, "user_id": {"type": "integer"}, "total_amount": {"type": "number", "format": "float"}, "created_at": {"type": "string", "format": "date-time"}, "items": {"type": "array", "items": ref("OrderItemInput")}}},
		},
	},
}


def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	app.openapi_schema = FAKESTORE_OPENAPI
	return app.openapi_schema


app.openapi = custom_openapi


app.include_router(products.router, prefix="/api")
app.include_router(carts.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(wishlists.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
