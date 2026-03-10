from sqlalchemy.orm import Session
from app.models import URL
from app.utils import generate_short_code


class URLService:

    def __init__(self, db: Session):
        self.db = db


    def create_short_url(self, original_url: str, alias: str = None):

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

        db_url = URL(
            original_url=original_url,
            short_code=code
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