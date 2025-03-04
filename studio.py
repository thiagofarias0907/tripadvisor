from typing import Any

from pydantic import BaseModel


class Studio(BaseModel):
    order: int
    name: str
    url: str
    n_reviews: int = 0
    score: float = None
    location: Any = None
    category: str


