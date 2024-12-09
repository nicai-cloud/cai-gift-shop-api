from dataclasses import dataclass


@dataclass
class Item:
    id: int
    image_src: str
    title: str
    price: float


@dataclass
class Preselection:
    id: int
    image_src: str
    title: str
    description: str
    price: float
    bag_id: int
    item_ids: list[int]
