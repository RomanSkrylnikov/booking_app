import asyncio
from datetime import date, datetime
from inspect import getfullargspec, signature

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.execptions import IncorrectParamsException
from app.hotels.dao import HotelDAO
from app.hotels.models import Hotels
from app.hotels.rooms.schemas import SAvailableRoom, SHotelWithRooms
from app.hotels.schemas import SAvailableHotel, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

filters = {"price": 4300}


@router.get("")
@cache(expire=30)
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date) -> list[SAvailableHotel]:
    await asyncio.sleep(3)
    res = await HotelDAO.find_available_hotels(location, date_from, date_to)
    return res


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(
        hotel_id: int,
        date_from: date,
        date_to: date) -> list[SAvailableRoom]:
    res = await HotelDAO.get_rooms_by_hotel(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    return res


@router.get("/id/{hotel_id}")
async def get_rooms_by_hotel(hotel_id: int) -> SHotel:
    id_filter = {"id": hotel_id}
    res = await HotelDAO.find_one_or_none(**id_filter)
    return res
