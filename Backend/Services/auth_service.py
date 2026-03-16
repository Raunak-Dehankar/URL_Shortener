from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
from fastapi import Security, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from Backend.database import SessionLocal
import secrets
from sqlalchemy.orm import Session
from Backend.Models.user import User


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

def get_db():

        db = SessionLocal()

        try:
            yield db

        finally:
            db.close()

class AuthService:

    def __init__(self, db: Session):
        self.db = db


    def verify_token(self, token: str):

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")

            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = self.db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user


    def hash_password(self, password: str):
        return pwd_context.hash(password[:72])


    def verify_password(self, plain, hashed):
        return pwd_context.verify(plain[:72], hashed)


    def create_access_token(self, data: dict):

        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return token

    
from Backend.database import get_db

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.verify_token(token)
