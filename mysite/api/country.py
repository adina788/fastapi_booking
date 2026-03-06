from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Country
from mysite.db.schema import CountrySchema
from typing import List

country_router = APIRouter(prefix='/country', tags=['country'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@country_router.post('/create', response_model=CountrySchema)
async def create_country(country_data: CountrySchema, db: Session = Depends(get_db)):
    country_db = Country(**country_data.dict())
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.get('/list', response_model=List[CountrySchema])
async def list_country(db: Session = Depends(get_db)):
    country_db = db.query(Country).all()
    return country_db

@country_router.get('/detail', response_model=CountrySchema)
async def detail_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday mamleket jok')
    return country_db

@country_router.put('/update')
async def update_country(country_id: int, country_data: CountrySchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday mamleket jok')
    for country_key, country_value in country_data.dict().items():
        setattr(country_db, country_key, country_value)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.delete('/delete')
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday mamleket jok')
    db.delete(country_db)
    db.commit()
    return {'message': 'success deleted'}