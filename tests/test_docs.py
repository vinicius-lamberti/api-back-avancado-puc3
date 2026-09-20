from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_redirects_to_docs():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_openapi_includes_fakestore_and_local_endpoints():
    schema = app.openapi()

    assert "/products" in schema["paths"]
    assert "/carts" in schema["paths"]
    assert "/users" in schema["paths"]
    assert "/auth/login" in schema["paths"]
    assert "/wishlists" in schema["paths"]
    assert "/orders" in schema["paths"]
    assert "Product" in schema["components"]["schemas"]
    assert "User" in schema["components"]["schemas"]
    assert "Wishlist" in schema["components"]["schemas"]
    assert "Order" in schema["components"]["schemas"]


def test_openapi_response_descriptions_match_route_errors():
    schema = app.openapi()

    assert schema["paths"]["/products/{id}"]["get"]["responses"]["404"]["description"] == "Produto não encontrado"
    assert schema["paths"]["/carts/{id}"]["get"]["responses"]["404"]["description"] == "Carrinho não encontrado"
    assert schema["paths"]["/users/{id}"]["get"]["responses"]["404"]["description"] == "Usuário não encontrado"
    assert schema["paths"]["/wishlists/{wishlist_id}"]["get"]["responses"]["404"]["description"] == "Wishlist não encontrada"
    assert schema["paths"]["/wishlists"]["post"]["responses"]["400"]["description"] == "Usuário já possui 4 wishlists"
    assert schema["paths"]["/wishlists/{wishlist_id}/items"]["post"]["responses"]["400"]["description"] == "Produto já está na wishlist"
    assert schema["paths"]["/orders"]["post"]["responses"]["400"]["description"] == "Pedido deve possuir itens"
    assert schema["paths"]["/orders/{order_id}"]["get"]["responses"]["404"]["description"] == "Pedido não encontrado"
    assert schema["paths"]["/auth/login"]["post"]["responses"]["401"]["description"] == "Falha na autenticação"
    assert schema["paths"]["/auth/login"]["post"]["responses"]["502"]["description"] == "FakeStoreAPI indisponível"
