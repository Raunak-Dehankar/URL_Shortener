from sqlalchemy.orm import Session
from Backend.Models.models import URL
from Backend.Services.utils import generate_short_code
from fastapi import HTTPException
from Backend.Models.user import User

class URLService:

    def __init__(self, db: Session):
        self.db = db


    def create_short_url(self, original_url: str, user_id: int, alias: str = None):

        user = self.db.query(User).filter(User.id == user_id).first()

        count = self.db.query(URL).filter(URL.user_id == user_id).count()

        if count >= user.url_limit:
            raise HTTPException(
                status_code=403,
                detail="URL limit reached")

        short_code = alias if alias else generate_short_code()

        new_url = URL(
            original_url=str,
            short_code=short_code,
            user_id=user_id 
    )

        if alias in [None, "", "string"]:
            alias = None

        if alias:
            # check if alias already exists
            existing = (
                self.db.query(URL)
                .filter(URL.short_code == alias)
                .first()
            )

            if existing:
                raise ValueError("Alias already in use")

            code = alias

        else:
            code = self._generate_unique_code()

       # Create DB object
        db_url = URL(
            original_url=original_url,
            short_code=code,
            user_id=user_id
    )

        self.db.add(db_url)
        self.db.commit()
        self.db.refresh(db_url)

        return db_url


    def get_original_url(self, code: str):

        return (
            self.db.query(URL)
            .filter(URL.short_code == code)
            .first()
        )


    def _generate_unique_code(self):

        while True:

            code = generate_short_code()

            existing = (
                self.db.query(URL)
                .filter(URL.short_code == code)
                .first()
            )

            if not existing:
                return code