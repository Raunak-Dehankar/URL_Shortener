from fastapi import FastAPI
from Backend.database import get_db, SessionLocal
from Backend.Models.user import User
from Backend.Services.auth_service import AuthService
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Frontend.UIRouter.ui_router import router as ui_router
from Backend.Routers.user_router import router as user_router
from Backend.Routers.url_router import router as url_router
from Backend.Routers.admin_router import router as admin_router
from Backend.Routers.redirect_router import router as redirect_router


BASE_URL = "http://127.0.0.1:8000"

app = FastAPI()

app.include_router(ui_router)
app.include_router(user_router)
app.include_router(url_router)
app.include_router(admin_router)
app.include_router(redirect_router)


app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")
templates = Jinja2Templates(directory="Frontend/templates")

def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()

    if not admin:
        auth_service = AuthService(db)
        admin = User(
            username="admin",
            password=auth_service.hash_password("admin123"),
            role="admin",
            url_limit=9999,
            is_active=True
        )
        db.add(admin)
        db.commit()

    db.close()


create_admin()