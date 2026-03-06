from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import ImageRoom
from mysite.db.schema import ImageRoomSchema
from typing import List

image_room_router = APIRouter(prefix='/image_room', tags=['image_room'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@image_room_router.post('/create', response_model=ImageRoomSchema)
async def create_image_room(image_room_data: ImageRoomSchema, db: Session = Depends(get_db)):
    image_room_db = ImageRoom(**image_room_data.dict())
    db.add(image_room_db)
    db.commit()
    db.refresh(image_room_db)
    return image_room_db

@image_room_router.get('/list', response_model=List[ImageRoomSchema])
async def list_image_room(db: Session = Depends(get_db)):
    image_room_db = db.query(ImageRoom).all()
    return image_room_db

@image_room_router.get('/detail', response_model=ImageRoomSchema)
async def detail_image_room(image_room_id: int, db: Session = Depends(get_db)):
    image_room_db = db.query(ImageRoom).filter(ImageRoom.id == image_room_id).first()
    if not image_room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday image room jok')
    return image_room_db

@image_room_router.put('/update')
async def update_image_room(image_room_id: int, image_room_data: ImageRoomSchema, db: Session = Depends(get_db)):
    image_room_db = db.query(ImageRoom).filter(ImageRoom.id == image_room_id).first()
    if not image_room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday image room jok')
    for image_room_key, image_room_value in image_room_data.dict().items():
        setattr(image_room_db, image_room_key, image_room_value)
    db.commit()
    db.refresh(image_room_db)
    return image_room_db

@image_room_router.delete('/delete')
async def delete_image_room(image_room_id: int, db: Session = Depends(get_db)):
    image_room_db = db.query(ImageRoom).filter(ImageRoom.id == image_room_id).first()
    if not image_room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday image room jok')
    db.delete(image_room_db)
    db.commit()
    return {'message': 'success deleted'}