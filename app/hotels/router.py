import asyncio
from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.schemas import HotelsInfoSchema
from app.hotels.service import HotelsService

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("/id/{hotel_id}")
@cache(expire=60)
async def get_hotel(hotel_id: int):
    await asyncio.sleep(3)
    return await HotelsService.find_by_id(hotel_id)


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str, date_from: date, date_to: date
) -> list[HotelsInfoSchema]:
    return await HotelsService.find_all(location, date_from, date_to)
