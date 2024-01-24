from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = '__all__'
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-user'


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    name = 'BooKings'
    name_plural = 'BooKings'
    icon = 'fa-solid fa-book'


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    name = 'Room name'
    name_plural = 'Hotel Rooms'
    icon = 'fa-solid fa-bed'


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = 'Hotel'
    name_plural = 'Hotels'
    icon = 'fa-solid fa-hotel'
