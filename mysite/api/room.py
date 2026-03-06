from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Room
from mysite.db.schema import RoomSchema
from typing import List

room_router = APIRouter(prefix='/room', tags=['room'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_router.post('/create', response_model=RoomSchema)
async def create_room(room_data: RoomSchema, db: Session = Depends(get_db)):
    room_db = Room(**room_data.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.get('/list', response_model=List[RoomSchema])
async def list_room(db: Session = Depends(get_db)):
    room_db = db.query(Room).all()
    return room_db

@room_router.get('/detail', response_model=RoomSchema)
async def detail_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday room jok')
    return room_db

@room_router.put('/update')
async def update_room(room_id: int, room_data: RoomSchema, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday room jok')
    for room_key, room_value in room_data.dict().items():
        setattr(room_db, room_key, room_value)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.delete('/delete')
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday room jok')
    db.delete(room_db)
    db.commit()
    return {'message': 'success deleted'}