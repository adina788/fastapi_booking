from .view import (UserProfileView, CountryView, CityView, ServiceView, HotelView, ImageHotelView,
                   RoomView, ImageRoomView, ReviewView, BookingView, RefreshTokenView)
from sqladmin import Admin
from fastapi import FastAPI
from mysite.db.database import engine

def setup_admin(app: FastAPI):
    admin = Admin(app, engine=engine)
    admin.add_view(UserProfileView)
    admin.add_view(CountryView)
    admin.add_view(CityView)
    admin.add_view(ServiceView)
    admin.add_view(HotelView)
    admin.add_view(ImageHotelView)
    admin.add_view(RoomView)
    admin.add_view(ImageRoomView)
    admin.add_view(ReviewView)
    admin.add_view(BookingView)
    admin.add_view(RefreshTokenView)


