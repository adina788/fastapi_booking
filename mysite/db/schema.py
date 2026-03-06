from pydantic import BaseModel
from .models import UserRole, RoomType, RoomStatus
from typing import Optional
from datetime import date

class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: Optional[int]
    phone_number: str
    profile_image: str | None
    role: UserRole
    password: str

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone_number: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class CountrySchema(BaseModel):
    country_name: str
    country_image: str | None


class CitySchema(BaseModel):
    city_name: str
    city_image: str | None


class ServiceSchema(BaseModel):
    service_name: str
    service_image: str


class HotelSchema(BaseModel):
    country_id: int
    city_id: int
    hotel_name: str
    hotel_image: str
    service_id: int
    address: str
    description: str
    owner_id: int


class ImageHotelSchema(BaseModel):
    hotel_id: int
    image: str


class RoomSchema(BaseModel):
    room_name: int
    hotel_id: int
    room_image: str
    room_type: RoomType
    room_status: RoomStatus
    price:  int


class ImageRoomSchema(BaseModel):
    room_id: int
    image: str


class ReviewSchema(BaseModel):
    user_id: int
    hotel_id: int
    comment: str | None
    stars: Optional[int]


class BookingSchema(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    grown_ups: int = 0
    children: int = 0


