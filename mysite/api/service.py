from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Service
from mysite.db.schema import ServiceSchema
from typing import List

service_router = APIRouter(prefix='/service', tags=['service'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@service_router.post('/create', response_model=ServiceSchema)
async def create_service(service_data: ServiceSchema, db: Session = Depends(get_db)):
    service_db = Service(**service_data.dict())
    db.add(service_db)
    db.commit()
    db.refresh(service_db)
    return service_db

@service_router.get('/list', response_model=List[ServiceSchema])
async def list_service(db: Session = Depends(get_db)):
    service_db = db.query(Service).all()
    return service_db

@service_router.get('/detail', response_model=ServiceSchema)
async def detail_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday service jok')
    return service_db

@service_router.put('/update')
async def update_service(service_id: int, service_data: ServiceSchema, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday service jok')
    for service_key, service_value in service_data.dict().items():
        setattr(service_db, service_key, service_value)
    db.commit()
    db.refresh(service_db)
    return service_db

@service_router.delete('/delete')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday service jok')
    db.delete(service_db)
    db.commit()
    return {'message': 'success deleted'}