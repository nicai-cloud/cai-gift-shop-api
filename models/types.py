from dataclasses import dataclass


@dataclass
class Item:
    id: int
    image_src: str
    name: str
    price: float


@dataclass
class Preselection:
    id: int
    image_src: str
    name: str
    description: str
    price: float
    bag_id: int
    item_ids: list[int]
