from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database import get_db
from Backend.Models.user import User
from Backend.Models.models import URL
from Backend.Services.auth_service import get_current_user

router = APIRouter()


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

    return db.query(URL).all()


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

    return {"message": "User disabled"}


@router.post("/admin/set_limit/{user_id}")
def set_limit(
    user_id: int,
    limit: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):

    if admin.role != "admin":
        raise HTTPException(403)

    user = db.query(User).filter(User.id == user_id).first()

    user.url_limit = limit
    db.commit()

    return {"message": "Limit updated"}