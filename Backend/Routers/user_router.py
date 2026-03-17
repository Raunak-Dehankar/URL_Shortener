from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database import get_db
from Backend.Models.user import User
from Backend.ViewModels.usercreate_schema import UserCreate
from Backend.ViewModels.userlogin_schema import UserLogin
from Backend.Services.auth_service import AuthService

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    auth_service = AuthService(db)

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth_service.hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    auth_service = AuthService(db)

    db_user = db.query(User).filter(User.username == data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not auth_service.verify_password(data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    if not db_user.is_active:
        raise HTTPException(403, "User disabled")

    token = auth_service.create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "role": db_user.role
    }