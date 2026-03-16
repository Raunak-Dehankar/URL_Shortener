from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from Backend.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    original_url = Column(String)
    short_code = Column(String, unique=True)
    clicks = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="client")  
    is_active = Column(Boolean, default=True)
    url_limit = Column(Integer, default=10)
