from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from Backend.database import get_db, SessionLocal
from Backend.schemas import URLRequest
from Backend.url_service import URLService
from Backend.database import get_db, engine
from Backend.models import Base, URL

from Backend.user import User
from Backend.schemas import UserCreate, UserLogin
from Backend.auth import hash_password, verify_password, create_access_token, verify_token

from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Backend.auth import get_current_user
from fastapi.responses import FileResponse

Base.metadata.create_all(bind=engine)

BASE_URL = "http://127.0.0.1:8000"

app = FastAPI()

app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")
templates = Jinja2Templates(directory="Frontend/templates")

db = SessionLocal()

admin = db.query(User).filter(User.username == "admin").first()

if not admin:
    admin = User(
        username="admin",
        password=hash_password("admin123"),
        role="admin",
        url_limit=9999,
        is_active=True
    )

    db.add(admin)
    db.commit()

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
    return FileResponse("Frontend/static/dashboard.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    )



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
def login(data: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    if not db_user.is_active:
        raise HTTPException(403,"User disabled")

    token = create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "role": db_user.role}

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

@app.get("/myurls")
def get_user_urls(
    db: Session = Depends(get_db),
    user = Depends(verify_token)
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


@app.delete("/delete/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_token)
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

@app.get("/admin")
def admin_page(request: Request, user: User = Depends(verify_token)):

    if user.role != "admin":
        raise HTTPException(403,"Admin only")

    return templates.TemplateResponse("admin.html", {"request":request})

@app.get("/admin/users")
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

@app.get("/admin/urls")
def get_all_urls(
    db: Session = Depends(get_db),
    user: User = Depends(verify_token)
):

    if user.role != "admin":
        raise HTTPException(403)

    urls = db.query(URL).all()

    return urls

@app.post("/admin/disable_user/{user_id}")
def disable_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(verify_token)
):

    if admin.role != "admin":
        raise HTTPException(403)

    user = db.query(User).filter(User.id == user_id).first()

    if user.role == "admin":
        raise HTTPException(403, "Cannot disable admin")

    user.is_active = False

    db.commit()

    return {"message":"User disabled"}

@app.post("/admin/set_limit/{user_id}")
def set_limit(
    user_id:int,
    limit:int,
    db:Session = Depends(get_db),
    admin:User = Depends(verify_token)
):

    if admin.role != "admin":
        raise HTTPException(403)

    user = db.query(User).filter(User.id == user_id).first()

    user.url_limit = limit

    db.commit()

    return {"message":"Limit updated"}

