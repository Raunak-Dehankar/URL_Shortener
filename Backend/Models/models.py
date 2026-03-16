from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from Backend.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    clicks = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")