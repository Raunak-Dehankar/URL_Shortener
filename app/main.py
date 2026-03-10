from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import URLRequest
from app.url_service import URLService
from app.database import get_db, engine
from app.models import Base

Base.metadata.create_all(bind=engine)

BASE_URL = "http://127.0.0.1:8000"

app = FastAPI()


@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):

    service = URLService(db)

    try:
        alias = request.validate_alias()
        url = service.create_short_url(request.url, alias)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "short_url": f"{BASE_URL}/{url.short_code}"
    }


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    service = URLService(db)
    url = service.get_original_url(short_code)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=url.original_url, status_code=307)