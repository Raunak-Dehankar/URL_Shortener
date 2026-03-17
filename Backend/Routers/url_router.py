from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database import get_db
from Backend.Models.models import URL
from Backend.ViewModels.URLrequest_schema import URLRequest
from Backend.Services.url_service import URLService
from Backend.Services.auth_service import get_current_user
from Backend.Models.user import User

router = APIRouter()

BASE_URL = "http://127.0.0.1:8000"


@router.post("/shorten")
def shorten_url(
    request: URLRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    service = URLService(db)

    try:
        alias = request.validate_alias()
        if not alias:
            alias = None

        url = service.create_short_url(
            request.url,
            user.id,
            alias
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "short_url": f"{BASE_URL}/{url.short_code}"
    }


@router.get("/myurls")
def get_user_urls(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    urls = db.query(URL).filter(URL.user_id == user.id).all()

    return [
        {
            "id": u.id,
            "original_url": u.original_url,
            "short_url": f"{BASE_URL}/{u.short_code}",
            "clicks": u.clicks
        }
        for u in urls
    ]


@router.delete("/delete/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    url = db.query(URL).filter(
        URL.id == url_id,
        URL.user_id == user.id
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    db.delete(url)
    db.commit()

    return {"message": "URL deleted"}