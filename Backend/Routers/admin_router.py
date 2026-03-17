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

templates = Jinja2Templates(directory="Frontend/templates")

@router.delete("/delete/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
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

@router.get("/admin")
def admin_page(request: Request, user: User = Depends(get_current_user)):

    if user.role != "admin":
        raise HTTPException(403,"Admin only")

    return templates.TemplateResponse("admin.html", {"request":request})

@router.get("/admin/users")
def get_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):

    if admin.role != "admin":
        raise HTTPException(403)

    users = db.query(User).all()

    result = []

    for u in users:

        urls = db.query(URL).filter(URL.user_id == u.id).all()

        result.append({
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "is_active": u.is_active,
            "url_limit": u.url_limit,
            "urls": [
                {
                    "short": url.short_code,
                    "original": url.original_url,
                    "clicks": url.clicks
                }
                for url in urls
            ]
        })

    return result

@router.get("/admin/urls")
def get_all_urls(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    if user.role != "admin":
        raise HTTPException(403)

    urls = db.query(URL).all()

    return urls

@router.post("/admin/disable_user/{user_id}")
def disable_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):

    if admin.role != "admin":
        raise HTTPException(403)

    user = db.query(User).filter(User.id == user_id).first()

    if user.role == "admin":
        raise HTTPException(403, "Cannot disable admin")

    user.is_active = False

    db.commit()

    return {"message":"User disabled"}

@router.post("/admin/set_limit/{user_id}")
def set_limit(
    user_id:int,
    limit:int,
    db:Session = Depends(get_db),
    admin:User = Depends(get_current_user)
):

    if admin.role != "admin":
        raise HTTPException(403)

    user = db.query(User).filter(User.id == user_id).first()

    user.url_limit = limit

    db.commit()

    return {"message":"Limit updated"}