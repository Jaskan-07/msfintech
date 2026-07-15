# Economic Indicators Dashboard

A full-stack economic intelligence app with a React UI, FastAPI backend, PostgreSQL database, and Liquibase-managed schema migrations.

## Stack

| Layer | Technology |
| --- | --- |
| UI | React, TypeScript, Vite |
| API | Python 3.11, FastAPI, SQLAlchemy |
| Database | PostgreSQL 16 |
| Migrations | Liquibase 4.25 |
| Containers | Docker Compose |

## Project Structure

```text
msfintech/
|-- backend/
|   |-- app/
|   |   |-- api/v1/endpoints/   # FastAPI route modules
|   |   |-- core/               # settings and security helpers
|   |   |-- db/                 # SQLAlchemy engine/session
|   |   |-- models/             # ORM models
|   |   `-- schemas/            # Pydantic schemas
|   |-- migration/              # Liquibase changelogs and SQL seeds
|   |-- Dockerfile
|   |-- docker-compose.yml      # backend + db + liquibase
|   `-- requirements.txt
|-- ui/
|   |-- src/
|   |-- Dockerfile
|   `-- nginx.conf
|-- docker-compose.yml          # full stack
`-- README.md
```

## Quick Start

From the repository root:

```bash
docker compose up -d --build
```

Services:

| Service | URL |
| --- | --- |
| UI | http://localhost:8081 |
| API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

The database credentials used by the compose files are:

| Field | Value |
| --- | --- |
| Database | `economic_indicators` |
| User | `postgres` |
| Password | `postgres` |

## Backend Only

```bash
cd backend
docker compose up -d --build
```

The backend compose file starts PostgreSQL, runs Liquibase, then starts FastAPI after migrations finish.

## Seeded Users

| Username | Password | Role |
| --- | --- | --- |
| `msadmin` | `all4one` | Admin |
| `janalyst` | `all4one` | Analyst |
| `rviewer` | `all4one` | Viewer |

## RBAC Seed Data

| Role | Permission |
| --- | --- |
| Admin | `user:write` |
| Analyst | `indicator:write` |
| Viewer | `dashboard:read` |

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | API health check |
| GET | `/` | Welcome message |
| POST | `/api/v1/auth/login` | Login and receive a bearer token |
| POST | `/api/v1/auth/register` | Register a user; defaults to Viewer role |
| GET | `/api/v1/auth/me` | Current user from bearer token |
| GET | `/api/v1/users` | List users |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/users/{user_id}` | Get user by id |
| PUT | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |
| GET | `/api/v1/rbac/roles` | List roles and permissions |
| GET | `/api/v1/rbac/permissions` | List permissions |

Login:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"msadmin","password":"all4one"}'
```

Current user:

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

List roles:

```bash
curl http://localhost:8000/api/v1/rbac/roles
```

## Migrations

Liquibase runs from `backend/migration/changelog/db.changelog-master.xml`, which includes `v1.0/schema.xml`.

The schema creates:

| Table | Purpose |
| --- | --- |
| `users` | Authentication users |
| `ms_roles` | RBAC roles |
| `ms_permissions` | RBAC permissions |
| `ms_role_permissions` | Role-to-permission mapping |

Manual validation:

```bash
cd backend
docker compose run --rm liquibase \
  --url=jdbc:postgresql://db:5432/economic_indicators \
  --username=postgres \
  --password=postgres \
  --changeLogFile=db.changelog-master.xml \
  validate
```

## Local Development

Backend:

```bash
cd backend
pip install -r requirements.txt

# PowerShell
$env:POSTGRES_SERVER="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="postgres"
$env:POSTGRES_DB="economic_indicators"
$env:PYTHONPATH=(Get-Location).Path

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

UI:

```bash
cd ui
npm install
npm run dev
```

## Troubleshooting

If Liquibase reports duplicate changelog file warnings, use the compose commands in this repo. They mount `backend/migration/changelog` directly at `/liquibase/changelog` and use `--changeLogFile=db.changelog-master.xml`.

If the backend starts before tables exist, rebuild and start through compose:

```bash
cd backend
docker compose up -d --build
```

If `/api/v1/auth/me` returns `401`, log in first and pass the returned `access_token` as a bearer token.
