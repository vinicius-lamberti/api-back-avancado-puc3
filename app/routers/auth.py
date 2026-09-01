import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
	username: str
	password: str


@router.post("/login")
async def login(payload: LoginPayload):
	try:
		async with httpx.AsyncClient(timeout=10.0) as client:
			response = await client.post(
				"https://fakestoreapi.com/auth/login",
				json=payload.model_dump(),
			)
			response.raise_for_status()
			return response.json()
	except httpx.HTTPStatusError as exc:
		status_code = exc.response.status_code
		raise HTTPException(status_code=status_code, detail="Falha na autenticação") from exc
	except httpx.RequestError as exc:
		raise HTTPException(status_code=502, detail="FakeStoreAPI indisponível") from exc
