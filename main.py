from typing import List, Type

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session
from pydantic import BaseModel

from core.database import engine, Base, SessionLocal
from core.models import URL
from core.tasks import check_url

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class URLCreate(BaseModel):
    url: str


class URLBase(BaseModel):
    id: int
    url: str
    is_active: bool
    last_status: str

    class Config:
        from_attributes = True


@app.post('/urls', response_model=URLBase)
def create_url(url_data: URLCreate, db: Session = Depends(get_db)) -> URL:
    url_exists: bool = db.query(exists().where(URL.url == url_data.url)).scalar()

    if url_exists:
        raise HTTPException(status_code=400, detail='This URL has already been saved :|')

    db_url = URL(url=url_data.url)

    try:
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
    except (Exception, ):
        raise HTTPException(status_code=400, detail='Failed to add a url :(')

    check_url.delay(db_url.id)

    return db_url


@app.get('/urls', response_model=List[URLBase])
def list_urls(db: Session = Depends(get_db)) -> List[Type[URL]]:
    return db.query(URL).all()
