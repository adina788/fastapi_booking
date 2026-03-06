from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Hotel
from mysite.db.schema import HotelSchema
from typing import List

hotel_router = APIRouter(prefix='/hotel', tags=['hotel'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_router.post('/create', response_model=HotelSchema)
async def create_hotel(hotel_data: HotelSchema, db: Session = Depends(get_db)):
    hotel_db = Hotel(**hotel_data.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.get('/list', response_model=List[HotelSchema])
async def list_hotel(db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).all()
    return hotel_db

@hotel_router.get('/detail', response_model=HotelSchema)
async def detail_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday hotel jok')
    return hotel_db

@hotel_router.put('/update')
async def update_hotel(hotel_id: int, hotel_data: HotelSchema, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday hotel jok')
    for hotel_key, hotel_value in hotel_data.dict().items():
        setattr(hotel_db, hotel_key, hotel_value)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db

@hotel_router.delete('/delete')
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday hotel jok')
    db.delete(hotel_db)
    db.commit()
    return {'message': 'success deleted'}