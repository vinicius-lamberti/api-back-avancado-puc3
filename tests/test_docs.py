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
