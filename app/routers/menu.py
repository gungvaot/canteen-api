from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.repository import repo
from app.schemas import Category, MenuItemCreate, MenuItemOut, MenuItemUpdate

router = APIRouter(prefix="/menu-items", tags=["Menu"])
ItemId = Annotated[int, Path(gt=0, description="Mã món")]


def get_or_404(item_id: int) -> dict:
    item = repo.get(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Không tìm thấy món id={item_id}")
    return item


def ensure_unique_name(name: str, exclude_id: int | None = None) -> None:
    found = repo.find_by_name(name)
    if found and found["id"] != exclude_id:  # BR1
        raise HTTPException(status.HTTP_409_CONFLICT,
                            f"Món '{name}' đã có trong thực đơn")


# ---------- Đọc dữ liệu (US1, US2) ----------
@router.get("", response_model=list[MenuItemOut], summary="Xem thực đơn")
def list_items(
    category: Category | None = None,
    available: bool | None = None,
    max_price: Annotated[int | None, Query(gt=0)] = None,
    sort: Literal["id", "price", "name"] = "id",
    order: Literal["asc", "desc"] = "asc",
):
    items = repo.list()
    if category:
        items = [i for i in items if i["category"] == category]
    if available is not None:
        items = [i for i in items if i["available"] == available]
    if max_price:
        items = [i for i in items if i["price"] <= max_price]
    return sorted(items, key=lambda i: i[sort], reverse=(order == "desc"))


@router.get("/{item_id}", response_model=MenuItemOut, summary="Chi tiết món")
def get_item(item_id: ItemId):
    return get_or_404(item_id)


# ---------- Ghi dữ liệu (US3, US4, US5) ----------
@router.post("", response_model=MenuItemOut,
             status_code=status.HTTP_201_CREATED, summary="Thêm món")
def create_item(payload: MenuItemCreate, response: Response):
    ensure_unique_name(payload.name)
    item = repo.add(payload.model_dump())
    response.headers["Location"] = f"/menu-items/{item['id']}"
    return item


@router.put("/{item_id}", response_model=MenuItemOut, summary="Sửa toàn bộ")
def replace_item(item_id: ItemId, payload: MenuItemCreate):
    get_or_404(item_id)
    ensure_unique_name(payload.name, exclude_id=item_id)
    return repo.update(item_id, payload.model_dump())


@router.patch("/{item_id}", response_model=MenuItemOut, summary="Sửa một phần")
def update_item(item_id: ItemId, payload: MenuItemUpdate):
    get_or_404(item_id)
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("name"):
        ensure_unique_name(changes["name"], exclude_id=item_id)
    return repo.update(item_id, changes)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Xóa món")
def delete_item(item_id: ItemId):
    get_or_404(item_id)
    repo.delete(item_id)
