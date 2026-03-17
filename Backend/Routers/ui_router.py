from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from Backend.Models.user import User
from Backend.Services.auth_service import get_current_user


router = APIRouter()

templates = Jinja2Templates(directory="Frontend/templates")

@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

"""@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    ) """