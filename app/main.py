from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import URLRequest
from app.url_service import URLService
from app.database import get_db, engine
from app.models import Base

from app.user import User
from app.schemas import UserCreate, UserLogin
from app.auth import hash_password, verify_password, create_access_token, verify_token

from fastapi.security import HTTPBearer
from fastapi import Security
from jose import jwt

Base.metadata.create_all(bind=engine)

BASE_URL = "http://127.0.0.1:8000"

app = FastAPI()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "user created"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token}

@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db), user = Depends(verify_token)):

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