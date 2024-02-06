from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.hashed_password]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = "__all__"
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-plane"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = "__all__"
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = "__all__"
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"
