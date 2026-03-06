from sqladmin import ModelView
from mysite.db.models import (UserProfile, Country, City, Service, Hotel, ImageHotel, Room,
                              ImageRoom, Review, Booking, RefreshToken)


class UserProfileView(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]

class CountryView(ModelView, model=Country):
    column_list = [Country.id, Country.country_name]

class CityView(ModelView, model=City):
    column_list = [City.id, City.city_name]

class ServiceView(ModelView, model=Service):
    column_list = [Service.id, Service.service_name]

class HotelView(ModelView, model=Hotel):
    column_list = [Hotel.id, Hotel.hotel_name]

class ImageHotelView(ModelView, model=ImageHotel):
    column_list = [ImageHotel.id, ImageHotel.image]

class RoomView(ModelView, model=Room):
    column_list = [Room.id, Room.room_type]

class ImageRoomView(ModelView, model=ImageRoom):
    column_list = [ImageRoom.id, ImageRoom.image]

class ReviewView(ModelView, model=Review):
    column_list = [Review.id, Review.user_id, Review.comment]

class BookingView(ModelView, model=Booking):
    column_list = [Booking.id, Booking.user_id]

class RefreshTokenView(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id]