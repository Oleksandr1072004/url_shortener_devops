import os
import pytest
from fastapi.testclient import TestClient

# Використовуємо окрему тестову БД, якщо задана (у CI)
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from app.main import app  # noqa: E402
from app.db import Base, engine  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_shorten_and_redirect():
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "code" in data
    assert data["short_url"].endswith(data["code"])

    # GET /{code} має повернути редірект (307) на оригінальний URL
    r2 = client.get(f"/{data['code']}", follow_redirects=False)
    assert r2.status_code in (302, 307)
    assert r2.headers["location"] == "https://example.com/"


def test_stats_increments_clicks():
    r = client.post("/shorten", json={"url": "https://openai.com"})
    code = r.json()["code"]

    # два переходи
    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)

    r_stats = client.get(f"/stats/{code}")
    assert r_stats.status_code == 200
    assert r_stats.json()["clicks"] == 2


def test_unknown_code_returns_404():
    r = client.get("/nonexistent", follow_redirects=False)
    assert r.status_code == 404