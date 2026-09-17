import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://shortener:secret@db:5432/shortener_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Analytics Service", version="1.0.0")


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), unique=True, index=True)
    original_url = Column(String(2048))
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats/total")
def total_stats(db: Session = Depends(get_db)):
    total_links = db.query(func.count(Link.id)).scalar() or 0
    total_clicks = db.query(func.coalesce(func.sum(Link.clicks), 0)).scalar() or 0
    return {"total_links": total_links, "total_clicks": total_clicks}


@app.get("/stats/top")
def top_links(limit: int = 5, db: Session = Depends(get_db)):
    rows = (
        db.query(Link)
        .order_by(Link.clicks.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "code": r.code,
            "original_url": r.original_url,
            "clicks": r.clicks,
        }
        for r in rows
    ]


@app.get("/stats/{code}")
def link_stats(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter_by(code=code).first()
    if not link:
        raise HTTPException(404, "Not found")
    return {
        "code": link.code,
        "original_url": link.original_url,
        "clicks": link.clicks,
        "created_at": link.created_at.isoformat(),
    }