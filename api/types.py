from dataclasses import dataclass


@dataclass
class Item:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    sub_category: str


@dataclass
class Preselection:
    id: int
    image_url: str
    name: str
    description: str
    price: float
    bag_id: int
    item_ids: list[int]


@dataclass
class Bag:
    id: int
    image_url: str
    name: str
    description: str
    size: str
    price: float
