from datetime import datetime


class MenuRepository:
    def __init__(self):
        self._items: dict[int, dict] = {}
        self._next_id = 1

    def list(self) -> list[dict]:
        return list(self._items.values())

    def get(self, item_id: int) -> dict | None:
        return self._items.get(item_id)

    def find_by_name(self, name: str) -> dict | None:
        return next((i for i in self._items.values()
                     if i["name"].lower() == name.lower()), None)

    def add(self, data: dict) -> dict:
        item = {"id": self._next_id, **data, "updated_at": datetime.now()}
        self._items[item["id"]] = item
        self._next_id += 1
        return item

    def update(self, item_id: int, data: dict) -> dict:
        self._items[item_id].update(data, updated_at=datetime.now())
        return self._items[item_id]

    def delete(self, item_id: int) -> None:
        del self._items[item_id]


repo = MenuRepository()
for seed in [
    {"name": "Cơm gà xối mỡ", "category": "com", "price": 35000},
    {"name": "Bún cá Hải Phòng", "category": "bun_pho", "price": 30000},
    {"name": "Bánh đa cua", "category": "bun_pho", "price": 30000,
     "available": False},
    {"name": "Trà chanh", "category": "do_uong", "price": 10000},
]:
    repo.add({"available": True, **seed})
