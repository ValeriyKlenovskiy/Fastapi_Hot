from datetime import date
from typing import List

from app.hotels.rooms.schemas import RoomsSchema
from app.hotels.rooms.service import RoomsService
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
    hotel_id: int, date_from: date, date_to: date
) -> List[RoomsSchema]:
    return await RoomsService.find_all(hotel_id, date_from, date_to)
