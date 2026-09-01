import httpx
from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/carts", tags=["carts"])
FAKESTORE_CARTS_URL = "https://fakestoreapi.com/carts"


async def _request(method: str, url: str, payload=None):
	try:
		async with httpx.AsyncClient(timeout=10.0) as client:
			response = await client.request(method, url, json=payload)
			if response.status_code == 404:
				raise HTTPException(status_code=404, detail="Carrinho não encontrado")
			response.raise_for_status()
			return response.json()
	except HTTPException:
		raise
	except httpx.HTTPError as exc:
		raise HTTPException(status_code=502, detail="FakeStoreAPI indisponível") from exc


@router.get("/{cart_id}")
async def get_cart(cart_id: int):
	return await _request("GET", f"{FAKESTORE_CARTS_URL}/{cart_id}")


@router.post("")
async def create_cart(payload: dict = Body(...)):
	return await _request("POST", FAKESTORE_CARTS_URL, payload)


@router.put("/{cart_id}")
async def update_cart(cart_id: int, payload: dict = Body(...)):
	return await _request("PUT", f"{FAKESTORE_CARTS_URL}/{cart_id}", payload)


@router.delete("/{cart_id}")
async def delete_cart(cart_id: int):
	return await _request("DELETE", f"{FAKESTORE_CARTS_URL}/{cart_id}")
