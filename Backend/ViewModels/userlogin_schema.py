from pydantic import BaseModel, Field
from typing import Optional
import re

class UserLogin(BaseModel):
    username: str
    password: str
