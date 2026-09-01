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
		"title": "FakeStoreAPI",
		"description": "A free fake API for testing and prototyping e-commerce applications.",
		"version": "v2.1.11",
		"contact": {
			"email": "support@fakestoreapi.com",
			"url": "https://fakestoreapi.com/docs",
		},
		"x-logo": {"url": "/icons/logo.png", "href": "/"},
	},
	"tags": [
		{"name": "Products", "x-displayName": "🛒 Products"},
		{"name": "Carts", "x-displayName": "🛍️ Carts"},
		{"name": "Users", "x-displayName": "👤 Users"},
		{"name": "Auth", "x-displayName": "🔒 Auth"},
		{"name": "Wishlists", "x-displayName": "💝 Wishlists"},
		{"name": "Orders", "x-displayName": "🧾 Orders"},
	],
	"servers": [{"url": "https://fakestoreapi.com"}],
	"paths": {
		"/products": {
			"get": {
				"summary": "Get all products",
				"description": "Retrieve a list of all available products.",
				"operationId": "getAllProducts",
				"tags": ["Products"],
				"responses": {
					"200": success_response("Product"),
					"400": {"description": BAD_REQUEST_DESCRIPTION},
				},
			},
			"post": {
				"summary": "Add a new product",
				"description": "Create a new product.",
				"operationId": "addProduct",
				"tags": ["Products"],
				"requestBody": {"required": True, "content": json_schema("Product")},
				"responses": {
					"201": {"description": "Product created successfully", "content": json_schema("Product")},
					"400": {"description": BAD_REQUEST_DESCRIPTION},
				},
			},
		},
		"/products/{id}": {
			"get": {
				"summary": "Get a single product",
				"description": "Retrieve details of a specific product by ID.",
				"operationId": "getProductById",
				"tags": ["Products"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {"200": success_response("Product"), "400": {"description": BAD_REQUEST_DESCRIPTION}},
			},
			"put": {
				"summary": "Update a product",
				"description": "Update an existing product by ID.",
				"operationId": "updateProduct",
				"tags": ["Products"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"requestBody": {"required": True, "content": json_schema("Product")},
				"responses": {"200": {"description": "Product updated successfully", "content": json_schema("Product")}, "400": {"description": BAD_REQUEST_DESCRIPTION}},
			},
			"delete": {
				"summary": "Delete a product",
				"description": "Delete a specific product by ID.",
				"operationId": "deleteProduct",
				"tags": ["Products"],
				"parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
				"responses": {"200": {"description": "Product deleted successfully"}, "400": {"description": BAD_REQUEST_DESCRIPTION}},
			},
		},
		"/carts": {
			"get": {"summary": "Get all carts", "description": "Retrieve a list of all available carts.", "operationId": "getAllCarts", "tags": ["Carts"], "responses": {"200": success_response("Cart"), "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"post": {"summary": "Add a new cart", "description": "Create a new cart.", "operationId": "addCart", "tags": ["Carts"], "requestBody": {"required": True, "content": json_schema("Cart")}, "responses": {"201": {"description": "Cart created successfully", "content": json_schema("Cart")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/carts/{id}": {
			"get": {"summary": "Get a single cart", "description": "Retrieve details of a specific cart by ID.", "operationId": "getCartById", "tags": ["Carts"], "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": success_response("Cart"), "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"put": {"summary": "Update a cart", "description": "Update an existing cart by ID.", "operationId": "updateCart", "tags": ["Carts"], "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}], "requestBody": {"required": True, "content": json_schema("Cart")}, "responses": {"200": {"description": "Cart updated successfully", "content": json_schema("Cart")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"delete": {"summary": "Delete a cart", "description": "Delete a specific cart by ID.", "operationId": "deleteCart", "tags": ["Carts"], "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": {"description": "Cart deleted successfully"}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/users": {
			"get": {"summary": "Get all users", "description": "Retrieve a list of all users.", "operationId": "getAllUsers", "tags": ["Users"], "responses": {"200": success_response("User"), "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"post": {"summary": "Add a new user", "description": "Create a new user.", "operationId": "addUser", "tags": ["Users"], "requestBody": {"required": True, "content": json_schema("User")}, "responses": {"201": {"description": "User created successfully", "content": json_schema("User")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/users/{id}": {
			"get": {"summary": "Get a single user", "description": "Retrieve details of a specific user by ID.", "operationId": "getUserById", "tags": ["Users"], "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": success_response("User"), "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"put": {"summary": "Update a user", "description": "Update an existing user by ID.", "operationId": "updateUser", "tags": ["Users"], "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}], "requestBody": {"required": True, "content": json_schema("User")}, "responses": {"200": {"description": "User updated successfully", "content": json_schema("User")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
			"delete": {"summary": "Delete a user", "description": "Delete a specific user by ID.", "operationId": "deleteUser", "tags": ["Users"], "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": {"description": "User deleted successfully"}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/auth/login": {
			"post": {"summary": "Login", "description": "Authenticate a user.", "operationId": "loginUser", "tags": ["Auth"], "requestBody": {"required": True, "content": json_schema("Login")}, "responses": {"200": {"description": "Login successful", "content": json_schema("LoginResponse")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/wishlists": {
			"post": {"summary": "Create a wishlist", "description": "Create a wishlist for a user.", "operationId": "createWishlist", "tags": ["Wishlists"], "requestBody": {"required": True, "content": json_schema("WishlistCreate")}, "responses": {"201": {"description": "Wishlist created", "content": json_schema("Wishlist")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/wishlists/user/{user_id}": {
			"get": {"summary": "List wishlists by user", "description": "Retrieve all wishlists for a specific user.", "operationId": "listUserWishlists", "tags": ["Wishlists"], "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": {"description": SUCCESS_DESCRIPTION, "content": {APPLICATION_JSON: {"schema": {"type": "array", "items": ref("Wishlist")}}}}}},
		},
		"/wishlists/{wishlist_id}": {
			"get": {"summary": "Get a wishlist", "description": "Retrieve a specific wishlist.", "operationId": "getWishlist", "tags": ["Wishlists"], "parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": success_response("Wishlist"), "404": {"description": WISHLIST_NOT_FOUND_DESCRIPTION}}},
			"put": {"summary": "Update a wishlist", "description": "Update a wishlist name.", "operationId": "updateWishlist", "tags": ["Wishlists"], "parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "requestBody": {"required": True, "content": json_schema("WishlistUpdate")}, "responses": {"200": success_response("Wishlist"), "404": {"description": WISHLIST_NOT_FOUND_DESCRIPTION}}},
			"delete": {"summary": "Delete wishlist", "description": "Delete a wishlist by ID.", "operationId": "deleteWishlist", "tags": ["Wishlists"], "parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"204": {"description": "Wishlist deleted"}, "404": {"description": WISHLIST_NOT_FOUND_DESCRIPTION}}},
		},
		"/wishlists/{wishlist_id}/items": {
			"post": {"summary": "Add item to wishlist", "description": "Add a product to a wishlist.", "operationId": "addWishlistItem", "tags": ["Wishlists"], "parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "requestBody": {"required": True, "content": json_schema("WishlistItemCreate")}, "responses": {"201": {"description": "Item created", "content": json_schema("WishlistItem")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/wishlists/{wishlist_id}/items/{product_id}": {
			"delete": {"summary": "Delete wishlist item", "description": "Remove an item from a wishlist.", "operationId": "deleteWishlistItem", "tags": ["Wishlists"], "parameters": [{"name": "wishlist_id", "in": "path", "required": True, "schema": {"type": "integer"}}, {"name": "product_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"204": {"description": "Item deleted"}, "404": {"description": "Item not found"}}},
		},
		"/orders": {
			"post": {"summary": "Create order", "description": "Create a new order for a user.", "operationId": "createOrder", "tags": ["Orders"], "requestBody": {"required": True, "content": json_schema("CreateOrderPayload")}, "responses": {"201": {"description": "Order created", "content": json_schema("Order")}, "400": {"description": BAD_REQUEST_DESCRIPTION}}},
		},
		"/orders/user/{user_id}": {
			"get": {"summary": "List orders by user", "description": "Retrieve orders for a specific user.", "operationId": "listUserOrders", "tags": ["Orders"], "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": {"description": SUCCESS_DESCRIPTION, "content": {APPLICATION_JSON: {"schema": {"type": "array", "items": ref("Order")}}}}}},
		},
		"/orders/{order_id}": {
			"get": {"summary": "Get order", "description": "Retrieve a specific order.", "operationId": "getOrder", "tags": ["Orders"], "parameters": [{"name": "order_id", "in": "path", "required": True, "schema": {"type": "integer"}}], "responses": {"200": success_response("Order"), "404": {"description": "Order not found"}}},
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
