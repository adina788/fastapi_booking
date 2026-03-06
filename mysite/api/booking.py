from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Booking
from mysite.db.schema import BookingSchema
from typing import List

booking_router = APIRouter(prefix='/booking', tags=['booking'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@booking_router.post('/create', response_model=BookingSchema)
async def create_booking(booking_data: BookingSchema, db: Session = Depends(get_db)):
    booking_db = Booking(**booking_data.dict())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.get('/list', response_model=List[BookingSchema])
async def list_booking(db: Session = Depends(get_db)):
    booking_db = db.query(Booking).all()
    return booking_db

@booking_router.get('/detail', response_model=BookingSchema)
async def detail_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday booking jok')
    return booking_db

@booking_router.put('/update')
async def update_booking(booking_id: int, booking_data: BookingSchema, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday booking jok')
    for booking_key, booking_value in booking_data.dict().items():
        setattr(booking_db, booking_key, booking_value)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@booking_router.delete('/delete')
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday booking jok')
    db.delete(booking_db)
    db.commit()
    return {'message': 'success deleted'}