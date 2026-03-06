from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import ImageHotel
from mysite.db.schema import ImageHotelSchema
from typing import List

image_hotel_router = APIRouter(prefix='/image_hotel', tags=['image_hotel'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@image_hotel_router.post('/create', response_model=ImageHotelSchema)
async def create_image_hotel(image_hotel_data: ImageHotelSchema, db: Session = Depends(get_db)):
    image_hotel_db = ImageHotel(**image_hotel_data.dict())
    db.add(image_hotel_db)
    db.commit()
    db.refresh(image_hotel_db)
    return image_hotel_db

@image_hotel_router.get('/list', response_model=List[ImageHotelSchema])
async def list_image_hotel(db: Session = Depends(get_db)):
    image_hotel_db = db.query(ImageHotel).all()
    return image_hotel_db

@image_hotel_router.get('/detail', response_model=ImageHotelSchema)
async def detail_image_hotel(image_hotel_id: int, db: Session = Depends(get_db)):
    image_hotel_db = db.query(ImageHotel).filter(ImageHotel.id == image_hotel_id).first()
    if not image_hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday image hotel jok')
    return image_hotel_db

@image_hotel_router.put('/update')
async def update_image_hotel(image_hotel_id: int, image_hotel_data: ImageHotelSchema, db: Session = Depends(get_db)):
    image_hotel_db = db.query(ImageHotel).filter(ImageHotel.id == image_hotel_id).first()
    if not image_hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday image hotel jok')
    for image_hotel_key, image_hotel_value in image_hotel_data.dict().items():
        setattr(image_hotel_db, image_hotel_key, image_hotel_value)
    db.commit()
    db.refresh(image_hotel_db)
    return image_hotel_db

@image_hotel_router.delete('/delete')
async def delete_image_hotel(image_hotel_id: int, db: Session = Depends(get_db)):
    image_hotel_db = db.query(ImageHotel).filter(ImageHotel.id == image_hotel_id).first()
    if not image_hotel_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday image hotel jok')
    db.delete(image_hotel_db)
    db.commit()
    return {'message': 'success deleted'}