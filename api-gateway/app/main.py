import os
import random
import string
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models
from .schemas import ShortenRequest, ShortenResponse, LinkStats

# Створюємо таблиці при старті (для лаби достатньо; у продакшені — Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API", version="1.0.0")

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
CODE_LENGTH = int(os.getenv("CODE_LENGTH", "6"))


def generate_code(n: int = CODE_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=n))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten(payload: ShortenRequest, db: Session = Depends(get_db)):
    # генеруємо унікальний код
    for _ in range(10):
        code = generate_code()
        if not db.query(models.Link).filter_by(code=code).first():
            break
    else:
        raise HTTPException(500, "Could not generate unique code")

    link = models.Link(code=code, original_url=str(payload.url), clicks=0)
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"code": code, "short_url": f"{BASE_URL}/{code}"}


@app.get("/stats/{code}", response_model=LinkStats)
def stats(code: str, db: Session = Depends(get_db)):
    link = db.query(models.Link).filter_by(code=code).first()
    if not link:
        raise HTTPException(404, "Not found")
    return link


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    link = db.query(models.Link).filter_by(code=code).first()
    if not link:
        raise HTTPException(404, "Not found")
    link.clicks += 1
    db.commit()
    return RedirectResponse(url=link.original_url)