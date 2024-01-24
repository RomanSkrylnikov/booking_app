from datetime import date

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class SAvailableHotel(SHotel):
    rooms_left: int
