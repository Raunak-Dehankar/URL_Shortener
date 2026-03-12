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

from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth import get_current_user
from fastapi.responses import FileResponse

Base.metadata.create_all(bind=engine)

BASE_URL = "http://127.0.0.1:8000"

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register-page")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):
    return FileResponse("static/dashboard.html")



@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

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
def shorten_url(
    request: URLRequest,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
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


@app.get("/{short_code}")
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