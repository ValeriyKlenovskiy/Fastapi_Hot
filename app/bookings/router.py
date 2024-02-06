from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.schemas import BookingsSchema
from app.bookings.service import BookingsService
from app.exceptions import (
    DateFromIsGreaterThenDateToException,
    RoomCanNotBeBookedException,
    TotalDaysIsGreaterThen30Exception,
)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["booking"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingsService.find_all_with_images(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    if date_from > date_to:
        raise DateFromIsGreaterThenDateToException
    if (
        datetime.strptime(str(date_to), "%Y-%m-%d") - relativedelta(days=30)
    ) > datetime.strptime(str(date_from), "%Y-%m-%d"):
        raise TotalDaysIsGreaterThen30Exception
    booking = await BookingsService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBookedException
    booking_dict = BookingsSchema.model_validate(booking).model_dump()
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingsService.delete(booking_id, user.id)
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
