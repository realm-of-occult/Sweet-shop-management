from typing import List, Optional

class Sweet:
    def __init__(self, sweet_id: int, name: str, category: str, price: float, quantity: int):
        self.id = sweet_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
        }

class SweetShop:
    def __init__(self):
        self.sweets = dict()  # key: id, value: Sweet

    def add_sweet(self, sweet: Sweet):
        if sweet.id in self.sweets:
            raise ValueError("Duplicate Sweet ID")
        self.sweets[sweet.id] = sweet

    def delete_sweet(self, sweet_id: int):
        if sweet_id not in self.sweets:
            raise ValueError("Sweet not found")
        del self.sweets[sweet_id]

    def view_sweets(self) -> List[Sweet]:
        return list(self.sweets.values())

    def search_sweets(self, name: Optional[str]=None, category: Optional[str]=None, 
                      price_min: Optional[float]=None, price_max: Optional[float]=None) -> List[Sweet]:
        result = self.sweets.values()
        if name:
            result = filter(lambda s: name.lower() in s.name.lower(), result)
        if category:
            result = filter(lambda s: category.lower() in s.category.lower(), result)
        if price_min is not None:
            result = filter(lambda s: s.price >= price_min, result)
        if price_max is not None:
            result = filter(lambda s: s.price <= price_max, result)
        return list(result)

    def sort_sweets(self, by: str="name") -> List[Sweet]:
        if by not in {"name", "category", "price"}:
            raise ValueError("Cannot sort by given field")
        return sorted(self.sweets.values(), key=lambda s: getattr(s, by))

    def purchase_sweet(self, sweet_id: int, qty: int):
        if sweet_id not in self.sweets:
            raise ValueError("Sweet not found")
        if self.sweets[sweet_id].quantity < qty:
            raise ValueError("Not enough stock")
        self.sweets[sweet_id].quantity -= qty

    def restock_sweet(self, sweet_id: int, qty: int):
        if sweet_id not in self.sweets:
            raise ValueError("Sweet not found")
        self.sweets[sweet_id].quantity += qty
