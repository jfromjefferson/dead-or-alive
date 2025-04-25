import datetime
from typing import Optional

import httpx
from core.models import URL
from core.database import SessionLocal
from core.celery_app import celery_app


@celery_app.task
def check_all_urls() -> None:
    with SessionLocal() as db:
        urls = db.query(URL).filter(URL.is_active == True).all() # noqa

        for url in urls:
            check_url.delay(url.id)


@celery_app.task
def check_url(url_id: int) -> None:
    with SessionLocal() as db:
        url: Optional[URL] = db.query(URL).filter(URL.id == url_id).first()

        if not url:
            return

        try:
            response = httpx.get(url.url, timeout=10)
            url.last_status = str(response.status_code)
        except (Exception, ):
            url.last_status = "DOWN"

        url.last_run = datetime.datetime.now()
        db.add(url)
        db.commit()
