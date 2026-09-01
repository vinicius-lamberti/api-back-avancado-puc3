from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.models import Wishlist, WishlistItem
from app.schemas.schemas import (
	WishlistCreate,
	WishlistItemCreate,
	WishlistItemSchema,
	WishlistSchema,
	WishlistUpdate,
)

router = APIRouter(prefix="/wishlists", tags=["wishlists"])


def _get_wishlist(db: Session, wishlist_id: int) -> Wishlist:
	wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
	if wishlist is None:
		raise HTTPException(status_code=404, detail="Wishlist não encontrada")
	return wishlist


@router.get("/user/{user_id}", response_model=list[WishlistSchema])
def list_wishlists(user_id: int, db: Session = Depends(get_db)):
	return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()


@router.get("/{wishlist_id}", response_model=WishlistSchema)
def get_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
	return _get_wishlist(db, wishlist_id)


@router.post("", response_model=WishlistSchema, status_code=201)
def create_wishlist(payload: WishlistCreate, db: Session = Depends(get_db)):
	count = db.query(Wishlist).filter(Wishlist.user_id == payload.user_id).count()
	if count >= 4:
		raise HTTPException(status_code=400, detail="Usuário já possui 4 wishlists")
	wishlist = Wishlist(user_id=payload.user_id, name=payload.name)
	db.add(wishlist)
	db.commit()
	db.refresh(wishlist)
	return wishlist


@router.put("/{wishlist_id}", response_model=WishlistSchema)
def update_wishlist(wishlist_id: int, payload: WishlistUpdate, db: Session = Depends(get_db)):
	wishlist = _get_wishlist(db, wishlist_id)
	wishlist.name = payload.name
	db.commit()
	db.refresh(wishlist)
	return wishlist


@router.delete("/{wishlist_id}", status_code=204)
def delete_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
	wishlist = _get_wishlist(db, wishlist_id)
	db.delete(wishlist)
	db.commit()


@router.post("/{wishlist_id}/items", response_model=WishlistItemSchema, status_code=201)
def add_item(wishlist_id: int, payload: WishlistItemCreate, db: Session = Depends(get_db)):
	_get_wishlist(db, wishlist_id)
	existing = db.query(WishlistItem).filter(
		WishlistItem.wishlist_id == wishlist_id,
		WishlistItem.product_id == payload.product_id,
	).first()
	if existing is not None:
		raise HTTPException(status_code=400, detail="Produto já está na wishlist")
	item = WishlistItem(wishlist_id=wishlist_id, product_id=payload.product_id)
	db.add(item)
	db.commit()
	db.refresh(item)
	return item


@router.delete("/{wishlist_id}/items/{product_id}", status_code=204)
def delete_item(wishlist_id: int, product_id: int, db: Session = Depends(get_db)):
	_get_wishlist(db, wishlist_id)
	item = db.query(WishlistItem).filter(
		WishlistItem.wishlist_id == wishlist_id,
		WishlistItem.product_id == product_id,
	).first()
	if item is None:
		raise HTTPException(status_code=404, detail="Item não encontrado")
	db.delete(item)
	db.commit()
