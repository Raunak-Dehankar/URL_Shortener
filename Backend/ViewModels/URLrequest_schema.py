from pydantic import BaseModel, Field
from typing import Optional
import re

class URLRequest(BaseModel):

    url: str
    alias: Optional[str] = Field(
        default=None,
        description="Optional custom alias (4-10 chars, letters/numbers/_/-)"
    )

    def validate_alias(self):
        if self.alias is None:
            return None

        pattern = r"^[a-zA-Z0-9_-]{4,10}$"

        if not re.match(pattern, self.alias):
            raise ValueError(
                "Alias must be 4-10 characters and contain only letters, numbers, _ or -"
            )

        return self.alias