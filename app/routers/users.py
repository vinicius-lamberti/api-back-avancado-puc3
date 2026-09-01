import httpx
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import UserUpdateSchema

router = APIRouter(prefix="/users", tags=["users"])
FAKESTORE_USERS_URL = "https://fakestoreapi.com/users"


async def _request(method: str, url: str, payload=None):
	try:
		async with httpx.AsyncClient(timeout=10.0) as client:
			response = await client.request(method, url, json=payload)
			if response.status_code == 404:
				raise HTTPException(status_code=404, detail="Usuário não encontrado")
			response.raise_for_status()
			return response.json()
	except HTTPException:
		raise
	except httpx.HTTPError as exc:
		raise HTTPException(status_code=502, detail="FakeStoreAPI indisponível") from exc


@router.get("/{user_id}")
async def get_user(user_id: int):
	return await _request("GET", f"{FAKESTORE_USERS_URL}/{user_id}")


@router.post("")
async def create_user(payload: UserUpdateSchema):
	return await _request("POST", FAKESTORE_USERS_URL, payload.model_dump(exclude_none=True))


@router.put("/{user_id}")
async def update_user(user_id: int, payload: UserUpdateSchema):
	return await _request("PUT", f"{FAKESTORE_USERS_URL}/{user_id}", payload.model_dump(exclude_none=True))
