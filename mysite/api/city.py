from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import City
from mysite.db.schema import CitySchema
from typing import List

city_router = APIRouter(prefix='/city', tags=['city'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.post('/create', response_model=CitySchema)
async def create_city(city_data: CitySchema, db: Session = Depends(get_db)):
    city_db = City(**city_data.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/list', response_model=List[CitySchema])
async def list_city(db: Session = Depends(get_db)):
    city_db = db.query(City).all()
    return city_db

@city_router.get('/detail', response_model=CitySchema)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday shaar jok')
    return city_db

@city_router.put('/update')
async def update_city(city_id: int, city_data: CitySchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday shaar jok')
    for city_key, city_value in city_data.dict().items():
        setattr(city_db, city_key, city_value)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.delete('/delete')
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday shaar jok')
    db.delete(city_db)
    db.commit()
    return {'message': 'success deleted'}