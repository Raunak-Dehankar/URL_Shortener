from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from Backend.database import get_db, SessionLocal
from Backend.Services.url_service import URLService
from Backend.database import get_db, engine
from Backend.Models.models import Base, URL

from Backend.Models.user import User
from Backend.ViewModels.usercreate_schema import UserCreate
from Backend.ViewModels.userlogin_schema import UserLogin
from Backend.ViewModels.URLrequest_schema import URLRequest

from Backend.Services.auth_service import AuthService, get_current_user

from fastapi import Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

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
    user = Depends(get_current_user)
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