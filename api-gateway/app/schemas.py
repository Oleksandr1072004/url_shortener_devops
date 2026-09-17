from pydantic import BaseModel, HttpUrl
from datetime import datetime


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    code: str
    short_url: str


class LinkStats(BaseModel):
    code: str
    original_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True