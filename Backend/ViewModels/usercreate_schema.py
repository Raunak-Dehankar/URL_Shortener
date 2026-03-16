from pydantic import BaseModel, Field
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    email: str
    password: str