from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.models import Order, OrderItem
from app.schemas.schemas import CreateOrderPayload, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


def _serialize_order(order: Order) -> dict:
	return {
		"id": order.id,
		"user_id": order.user_id,
		"total_amount": order.total_amount,
		"created_at": order.created_at,
		"items": [
			{
				"product_id": item.product_id,
				"quantity": item.quantity,
				"price_at_purchase": item.price_at_purchase,
			}
			for item in order.items
		],
	}


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(payload: CreateOrderPayload, db: Session = Depends(get_db)):
	if not payload.items:
		raise HTTPException(status_code=400, detail="Pedido deve possuir itens")
	total = sum(item.quantity * item.price_at_purchase for item in payload.items)
	order = Order(user_id=payload.user_id, total_amount=total)
	order.items = [
		OrderItem(
			product_id=item.product_id,
			quantity=item.quantity,
			price_at_purchase=item.price_at_purchase,
		)
		for item in payload.items
	]
	db.add(order)
	db.commit()
	db.refresh(order)
	return _serialize_order(order)


@router.get("/user/{user_id}", response_model=list[OrderResponse])
def list_user_orders(user_id: int, db: Session = Depends(get_db)):
	orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
	return [_serialize_order(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.id == order_id).first()
	if order is None:
		raise HTTPException(status_code=404, detail="Pedido não encontrado")
	return _serialize_order(order)
