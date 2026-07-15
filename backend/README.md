# Economic Indicators Backend

FastAPI backend for authentication, RBAC, and economic dashboard APIs. PostgreSQL schema changes are managed by Liquibase.

## Quick Start

```bash
docker compose up -d --build
```

This starts:

| Service | Purpose |
| --- | --- |
| `db` | PostgreSQL 16 |
| `liquibase` | Applies database migrations |
| `backend` | FastAPI on http://localhost:8000 |

API docs are available at http://localhost:8000/docs.

## Database

Compose credentials:

| Field | Value |
| --- | --- |
| Host from host machine | `localhost` |
| Host from containers | `db` |
| Port | `5432` |
| Database | `economic_indicators` |
| User | `postgres` |
| Password | `postgres` |

## Migrations

Main changelog:

```text
migration/changelog/db.changelog-master.xml
```

Included schema:

```text
migration/changelog/v1.0/schema.xml
```

Created tables:

| Table | Purpose |
| --- | --- |
| `users` | App users |
| `ms_roles` | Roles such as Admin, Analyst, Viewer |
| `ms_permissions` | Permission catalog |
| `ms_role_permissions` | Role-permission mapping |

Seeded users:

| Username | Password | Role |
| --- | --- | --- |
| `msadmin` | `all4one` | Admin |
| `janalyst` | `all4one` | Analyst |
| `rviewer` | `all4one` | Viewer |

Validate migrations:

```bash
docker compose run --rm liquibase \
  --url=jdbc:postgresql://db:5432/economic_indicators \
  --username=postgres \
  --password=postgres \
  --changeLogFile=db.changelog-master.xml \
  validate
```

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| POST | `/api/v1/auth/login` | Login and get a bearer token |
| POST | `/api/v1/auth/register` | Register user with Viewer role |
| GET | `/api/v1/auth/me` | Current authenticated user |
| GET | `/api/v1/users` | List users |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/users/{user_id}` | Get user by id |
| PUT | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |
| GET | `/api/v1/rbac/roles` | List roles with permissions |
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

Roles:

```bash
curl http://localhost:8000/api/v1/rbac/roles
```

## Local Development

```bash
pip install -r requirements.txt
```

PowerShell:

```powershell
$env:POSTGRES_SERVER="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="postgres"
$env:POSTGRES_DB="economic_indicators"
$env:PYTHONPATH=(Get-Location).Path

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Checks

```bash
python -m compileall app
docker compose config
docker compose run --rm liquibase --changeLogFile=db.changelog-master.xml validate
```
