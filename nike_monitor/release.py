from dataclasses import dataclass


@dataclass
class Release:
    sku: str
    exclusive_access: bool
    title: str
    price: float
    currency: str
    type: str
    date: str
    image: str
    sizes_with_stock: list[str]
