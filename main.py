from fastapi import FastAPI
from mysite.api import (user_profile, country, city, service, hotel, image_hotel, room, image_room,
                        review, booking, auth)
from mysite.admin.setup import setup_admin

booking_app = FastAPI(title='Booking_AI25')
booking_app.include_router(user_profile.user_router)
booking_app.include_router(country.country_router)
booking_app.include_router(city.city_router)
booking_app.include_router(service.service_router)
booking_app.include_router(hotel.hotel_router)
booking_app.include_router(image_hotel.image_hotel_router)
booking_app.include_router(room.room_router)
booking_app.include_router(image_room.image_room_router)
booking_app.include_router(review.review_router)
booking_app.include_router(booking.booking_router)
booking_app.include_router(auth.auth_router)

setup_admin(booking_app)




