from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database import get_db
from Backend.Services.url_service import URLService
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    if short_code == "favicon.ico":
        raise HTTPException(status_code=404)

    service = URLService(db)

    url = service.get_original_url(short_code)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.original_url)