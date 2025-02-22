from pydantic import BaseModel, Field
from datetime import datetime
from schemas.query_base import QueryBase


class HabitCreate(BaseModel):
  name: str = Field(...)
  code: str = Field(...)
  description: str = Field(...)
  categories: list[str] = Field(...)


class HabitUpdate(BaseModel):
  name: str = Field(...)
  code: str = Field(...)
  description: str = Field(...)
  categories: list[str] = Field(...)


class HabitCreateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(...)
  description: str = Field(...)
  categories: list[str] = Field(...)
  purchase_price: float = Field(...)
  sale_price: float = Field(...)
  stock: int = Field(default=0)
  created_at: datetime = None
  updated_at: datetime = None


class HabitUpdateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(...)
  description: str = Field(...)
  categories: list[str] = Field(...)


class HabitQuery(QueryBase):
  name: str = None
  code: str = None
  categories: list[str] = None
  in_stock: bool = None


class HabitListResponse(BaseModel):
  total: int = Field(...)
  items: list[HabitCreateResponse] = Field(...)
