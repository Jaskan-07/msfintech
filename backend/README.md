# Economic Indicators Dashboard - Backend

FastAPI backend service with JWT authentication and PostgreSQL database.

> **Full deployment instructions:** See [Root README](../README.md)

---

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Database Migrations](#database-migrations)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI entry point
│   ├── api/
│   │   └── v1/
│   │       ├── router.py           # API router
│   │       └── endpoints/
│   │           └── auth.py         # Auth endpoints
│   ├── core/
│   │   ├── config.py               # Settings
│   │   └── security.py             # JWT utilities
│   ├── db/
│   │   ├── base.py                 # SQLAlchemy base
│   │   └── session.py              # DB session
│   ├── models/
│   │   └── user.py                 # User model
│   └── schemas/
│       └── auth.py                 # Pydantic schemas
├── migration/
│   ├── liquibase.properties
│   └── changelog/
│       ├── db.changelog-master.xml
│       └── v1.0/
│           ├── schema.xml
│           └── postgres/
│               └── seed-admin-user.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                            # Environment variables
└── README.md
```

---

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Runtime |
| PostgreSQL | 16+ | Database |
| Docker/Podman | Latest | Liquibase migrations |

---

## Quick Start

### Option 1: Docker Compose

```bash
cd backend
docker compose up -d
```

### Option 2: Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (see Configuration section)

# 3. Run migrations (see Database Migrations section)

# 4. Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## API Documentation

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Welcome message | No |
| GET | `/health` | Health check | No |
| POST | `/api/v1/auth/login` | User login | No |
| POST | `/api/v1/auth/register` | Register user | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |

### Login

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "msadmin", "password": "all4one"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Register

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "full_name": "New User"
  }'
```

### Get Current User

**Request:**
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

## Database Migrations

### Using Docker

```bash
docker run --rm --network host \
  -v "$(pwd)/migration:/liquibase/changelog" \
  liquibase/liquibase:4.25-alpine \
  --url=jdbc:postgresql://localhost:5432/economic_indicators \
  --username=postgres --password=all4one \
  --changeLogFile=changelog/db.changelog-master.xml update
```

### Using Podman

```bash
podman run --rm --network host \
  -v "./migration:/liquibase/changelog:Z" \
  liquibase/liquibase:4.25-alpine \
  --url=jdbc:postgresql://localhost:5432/economic_indicators \
  --username=postgres --password=all4one \
  --changeLogFile=changelog/db.changelog-master.xml update
```

> **Windows Podman Note:** Use host gateway IP instead of localhost.
> See [Root README](../README.md#3-local-development-setup) for details.

### Migration Files

| File | Description |
|------|-------------|
| `db.changelog-master.xml` | Master changelog |
| `v1.0/schema.xml` | Users table + seed data |

### Rollback

```bash
# Rollback last changeset
liquibase rollback-count 1
```

---

## Configuration

### Environment Variables

Create `.env` file or set environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_SERVER` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `all4one` |
| `POSTGRES_DB` | Database name | `economic_indicators` |
| `SECRET_KEY` | JWT signing key | (generate for production) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL | `30` |

### Windows PowerShell

```powershell
$env:POSTGRES_SERVER="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="all4one"
$env:POSTGRES_DB="economic_indicators"
$env:PYTHONPATH=(Get-Location).Path
```

### Linux/macOS

```bash
export POSTGRES_SERVER=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=all4one
export POSTGRES_DB=economic_indicators
export PYTHONPATH=$(pwd)
```

---

## Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Development Server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Code Structure

| Module | Purpose |
|--------|---------|
| `app/main.py` | FastAPI app, CORS, routers |
| `app/core/config.py` | Pydantic Settings |
| `app/core/security.py` | JWT token creation |
| `app/db/session.py` | SQLAlchemy engine, session |
| `app/models/user.py` | User ORM model |
| `app/schemas/auth.py` | Request/response schemas |
| `app/api/v1/endpoints/auth.py` | Auth routes |

---

## Testing

### Test Health

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status": "healthy", "service": "economic-indicators-api"}
```

### Test Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "msadmin", "password": "all4one"}'
```

### Default Admin User

| Field | Value |
|-------|-------|
| Username | `msadmin` |
| Password | `all4one` |
| Email | `msadmin@economic-dashboard.com` |

---

## Troubleshooting

### Database Connection Error

**Error:** `password authentication failed for user "postgres"`

**Solutions:**
1. Verify `POSTGRES_PASSWORD` environment variable
2. Check PostgreSQL is running
3. Confirm database exists: `psql -U postgres -c "\l"`

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/backend
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# Kill process or use different port
python -m uvicorn app.main:app --port 8001
```

---

## Docker

### Build Image

```bash
docker build -t economic-indicators-api .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e POSTGRES_SERVER=host.docker.internal \
  -e POSTGRES_PASSWORD=all4one \
  economic-indicators-api
```

---

## License

MIT License