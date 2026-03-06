from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum,ForeignKey,Text,SmallInteger, Boolean
from typing import Optional,List
from enum import Enum as PyEnum
from datetime import date
from sqlalchemy import Date


class UserRole(str, PyEnum):
    client = 'client'
    owner = 'owner'

class RoomType(str, PyEnum):
    Семейный =  'Семейный'
    Одноместный = 'Одноместный'
    Двухместный = 'Двухместный'
    Люкс = 'Люкс'

class RoomStatus(str, PyEnum):
    Свободень = 'Свободень'
    Забронирован = 'Забронирован'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[str] = mapped_column(String)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.client)
    password: Mapped[str] = mapped_column(String)

    owner_hotels: Mapped['Hotel'] = relationship('Hotel', back_populates='owner',
                                          cascade='all, delete-orphan')
    user_review: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                       cascade='all, delete-orphan')
    user_booking: Mapped['Booking'] = relationship('Booking', back_populates='user',
                                                   cascade='all, delete-orphan')
    refresh_token: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                               cascade='all, delete-orphan')


class  RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='refresh_token')


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    country_name: Mapped[str] = mapped_column(String(35), unique=True)
    country_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    country: Mapped[List['Hotel']] = relationship('Hotel', back_populates='country',
                                                  cascade='all, delete-orphan')

    def __repr__(self):
        return self.country_name


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    city_name: Mapped[str] = mapped_column(String(35), unique=True)
    city_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    city: Mapped[List['Hotel']] = relationship('Hotel', back_populates='city',
                                               cascade='all, delete-orphan')

    def __repr__(self):
        return self.city_name


class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(35))
    service_image: Mapped[str] = mapped_column(String)

    service: Mapped[List['Hotel']] = relationship('Hotel', back_populates='service',
                                                  cascade='all, delete-orphan')

    def __repr__(self):
        return self.service_name


class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    hotel_name: Mapped[str] = mapped_column(String(50))
    hotel_image: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String(50))
    service_id: Mapped[str] = mapped_column(ForeignKey('service.id'))
    description: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[str] = mapped_column(ForeignKey('user_profile.id'))

    country: Mapped['Country'] = relationship('Country', back_populates='country')
    city: Mapped['City'] = relationship('City', back_populates='city')
    service: Mapped['Service'] = relationship('Service', back_populates='service')
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='owner_hotels')

    image_hotel: Mapped[List['ImageHotel']] = relationship('ImageHotel', back_populates='hotel',
                                                     cascade='all, delete-orphan')
    hotel_room: Mapped[List['Room']] = relationship('Room', back_populates='hotel',
                                               cascade='all, delete-orphan')
    hotel_review: Mapped[List['Review']] = relationship('Review', back_populates='hotel')
    hotel_booking: Mapped[List['Booking']] = relationship('Booking', back_populates='hotel',
                                                          cascade='all, delete-orphan')



class ImageHotel(Base):
    __tablename__ = 'image_hotel'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    image: Mapped[str] = mapped_column(String)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='image_hotel')


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_name: Mapped[int] = mapped_column(SmallInteger, default=0)
    room_image: Mapped[str] = mapped_column(String)
    room_type: Mapped[RoomType] = mapped_column(Enum(RoomType), default=RoomType.Одноместный)
    room_status: Mapped[RoomStatus] = mapped_column(Enum(RoomStatus), default=RoomStatus.Свободень)
    price: Mapped[int] = mapped_column(SmallInteger, default=0)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='hotel_room')

    image_room: Mapped[List['ImageRoom']] = relationship('ImageRoom', back_populates='room',
                                                   cascade='all, delete-orphan')
    room_booking: Mapped[List['Booking']] = relationship('Booking', back_populates='room',
                                                         cascade='all, delete-orphan')



class ImageRoom(Base):
    __tablename__ = 'image_room'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    image: Mapped[str] = mapped_column(String)

    room: Mapped["Room"] = relationship('Room', back_populates='image_room')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stars: Mapped[Optional[int]] = mapped_column(SmallInteger,nullable=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_review')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='hotel_review')


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    check_in_date: Mapped[date] = mapped_column(Date)
    check_out_date: Mapped[date] = mapped_column(Date)
    grown_ups: Mapped[int] = mapped_column(Integer, default=0)
    children: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_booking')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='hotel_booking')
    room: Mapped['Room'] = relationship('Room', back_populates='room_booking')

