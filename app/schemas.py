from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["com", "bun_pho", "do_uong", "an_vat"]  # BR3


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100,
                      examples=["Cơm gà xối mỡ"])
    category: Category
    price: int = Field(gt=0, le=200_000, multiple_of=1000)  # BR2
    available: bool = True  # BR4


class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: Category | None = None
    price: int | None = Field(default=None, gt=0, le=200_000,
                              multiple_of=1000)
    available: bool | None = None


class MenuItemOut(MenuItemCreate):
    id: int
    updated_at: datetime
