from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# FakeStore Proxy Schemas
class ProductSchema(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str


class CartItemSchema(BaseModel):
    productId: int
    quantity: int


class CartSchema(BaseModel):
    id: int
    userId: int
    date: Optional[str] = None
    products: List[CartItemSchema]


class UserUpdateSchema(BaseModel):
    username: str
    email: str
    password: Optional[str] = None


# Wishlist Schemas (SQLite)
class WishlistItemCreate(BaseModel):
    product_id: int


class WishlistItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    added_at: datetime


class WishlistCreate(BaseModel):
    user_id: int
    name: str


class WishlistUpdate(BaseModel):
    name: str


class WishlistSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    items: List[WishlistItemSchema] = Field(default_factory=list)


# Order Schemas (SQLite)
class OrderItemInput(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float


class CreateOrderPayload(BaseModel):
    user_id: int
    items: List[OrderItemInput]


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemInput]