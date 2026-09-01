import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/products", tags=["products"])
FAKESTORE_PRODUCTS_URL = "https://fakestoreapi.com/products"
FAKESTORE_UNAVAILABLE_DETAIL = "FakeStoreAPI indisponível"


@router.get("")
async def list_products():
	try:
		async with httpx.AsyncClient(timeout=10.0) as client:
			response = await client.get(FAKESTORE_PRODUCTS_URL)
			response.raise_for_status()
			return response.json()
	except httpx.HTTPError as exc:
		raise HTTPException(status_code=502, detail=FAKESTORE_UNAVAILABLE_DETAIL) from exc


@router.get("/{product_id}")
async def get_product(product_id: int):
	try:
		async with httpx.AsyncClient(timeout=10.0) as client:
			response = await client.get(f"{FAKESTORE_PRODUCTS_URL}/{product_id}")
			if response.status_code == 404:
				raise HTTPException(status_code=404, detail="Produto não encontrado")
			response.raise_for_status()
			return response.json()
	except httpx.HTTPStatusError as exc:
		raise HTTPException(status_code=502, detail=FAKESTORE_UNAVAILABLE_DETAIL) from exc
	except httpx.RequestError as exc:
		raise HTTPException(status_code=502, detail=FAKESTORE_UNAVAILABLE_DETAIL) from exc
