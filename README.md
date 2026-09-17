# URL Shortener — DevOps Lab 1

Мікросервісний застосунок для скорочення URL з PostgreSQL та Docker Compose.

## Архітектура

- **api-gateway** (FastAPI, :8000) — створює короткі посилання, редіректить, рахує кліки
- **analytics-service** (FastAPI, :8001) — агрегована статистика
- **db** (PostgreSQL 16) — спільна база даних

## Швидкий старт

```bash
cp .env.example .env
docker compose up --build
```

## Ендпоінти

### api-gateway (http://localhost:8000)

| Метод | Шлях | Опис |
|---|---|---|
| GET | `/health` | Перевірка стану |
| POST | `/shorten` | Тіло: `{"url": "https://..."}` → `{code, short_url}` |
| GET | `/{code}` | Редірект на оригінальний URL |
| GET | `/stats/{code}` | Статистика конкретного коду |

### analytics-service (http://localhost:8001)

| Метод | Шлях | Опис |
|---|---|---|
| GET | `/health` | Перевірка стану |
| GET | `/stats/total` | Всього посилань і кліків |
| GET | `/stats/top?limit=5` | Топ посилань за кліками |
| GET | `/stats/{code}` | Статистика коду |

## Приклад використання

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

curl -L http://localhost:8000/<code>

curl http://localhost:8001/stats/total
```

## Тести

```bash
docker compose exec api-gateway pytest -v
```

## Стек

- Python 3.11, FastAPI, SQLAlchemy 2, PostgreSQL 16
- Docker, Docker Compose
- Pytest, httpx