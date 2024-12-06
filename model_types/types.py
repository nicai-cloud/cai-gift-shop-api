from dataclasses import dataclass


@dataclass
class Customer:
    id: str
    first_name: str
    last_name: str
    email: str
    mobile: str
    address: str
