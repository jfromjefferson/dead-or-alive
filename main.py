import datetime
from typing import List, Type, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session
from pydantic import BaseModel

from core.database import SessionLocal
from core.models import URL
from core.tasks import check_url

app = FastAPI()


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class URLCreate(BaseModel):
    name: str
    url: str


class URLUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None


class URLBase(BaseModel):
    id: int
    name: str
    url: str
    is_active: bool
    last_status: str
    last_run: Optional[datetime.datetime]
    created_at: datetime.datetime

    class Config:
        from_attributes = True


@app.get('/urls', response_model=List[URLBase])
def list_urls(db: Session = Depends(get_db)) -> List[Type[URL]]:
    return db.query(URL).all()


@app.post('/urls', response_model=URLBase)
def create_url(url_data: URLCreate, db: Session = Depends(get_db)) -> URL:
    url_exists: bool = db.query(exists().where(URL.url == url_data.url)).scalar()

    if url_exists:
        raise HTTPException(status_code=400, detail='This URL has already been saved :|')

    db_url = URL(
        name=url_data.name,
        url=url_data.url
    )

    try:
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
    except (Exception, ):
        raise HTTPException(status_code=400, detail='Failed to add a url :(')

    if db_url.is_active:
        check_url.delay(db_url.id)

    return db_url


@app.patch('/urls/{id}', response_model=URLBase)
def update_url(id: int, url_data: URLUpdate, db: Session = Depends(get_db)) -> URL:
    db_url: Optional[URL] = db.query(URL).filter(URL.id == id).first()

    if not db_url:
        raise HTTPException(status_code=404, detail='URL does not exist')

    data: dict = url_data.model_dump(exclude_unset=True, exclude_none=True, exclude_defaults=True)

    for key, value in data.items():
        setattr(db_url, key, value)

    try:
        db.commit()
        db.refresh(db_url)
    except (Exception, ):
        raise HTTPException(status_code=400, detail='Failed to update a url :(')

    if db_url.is_active:
        check_url.delay(db_url.id)

    return db_url
