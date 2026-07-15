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

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Roles and Access Control](#roles-and-access-control)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

### Features

| Feature | Description |
|---------|-------------|
| User Authentication | Username/password login with HTTP Basic Auth for protected Swagger APIs |
| Economic Indicators | GDP, CPI, PCI, Unemployment rates |
| Financial Markets | Bond yields, Stock indices, Commodities |
| Real-time Data | Live API integrations |
| Responsive UI | Desktop and mobile support |

### Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | React, TypeScript, Vite | 18.x |
| Backend | Python, FastAPI, SQLAlchemy | 3.11+ |
| Database | PostgreSQL | 16+ |
| Migrations | Liquibase | 4.25 |
| Containers | Docker / Podman | Latest |

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │────▶│   FastAPI       │────▶│   PostgreSQL    │
│   Port: 3000*   │     │   Port: 8000    │     │   Port: 5432    │
│   Port: 8081**  │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        │                       ▼
        │               ┌─────────────────┐
        │               │   Liquibase     │
        │               │   Migrations    │
        │               └─────────────────┘
        │
        └──────────────▶ Vite Dev Proxy (/api → :8000)

* Development mode
** Production (Docker/Podman)
```

### Project Structure

```
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

See [Deployment Options](#deployment-options) for detailed instructions.

### Default Credentials

| Username | Password |
|----------|----------|
| `msadmin` | `all4one` |

---

## Deployment Options

### 1. Docker Compose Deployment

**Start Services:**
```bash
docker compose up -d
```

**View Logs:**
```bash
docker compose logs -f
```

**Stop Services:**
```bash
docker compose down      # Keep data
docker compose down -v   # Remove data
```

---

### 2. Podman Deployment

#### Install Podman

| OS | Command |
|----|---------|
| Windows | `winget install RedHat.Podman` |
| Ubuntu/Debian | `sudo apt install -y podman podman-compose` |
| RHEL/Fedora | `sudo dnf install -y podman podman-compose` |
| macOS | `brew install podman && podman machine init && podman machine start` |

#### Deploy with Podman Compose

```bash
podman-compose up -d
podman-compose logs -f
podman-compose down
```

#### Deploy with Podman Pod (Manual)

```bash
# Create pod
podman pod create --name economic-pod -p 8000:8000 -p 8081:8081 -p 5432:5432

# Start PostgreSQL
podman run -d --pod economic-pod --name economic-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=economic_indicators \
  postgres:16-alpine

# Wait for database
sleep 5

# Run migrations (replace HOST_IP with your machine's IP for Podman VM)
podman run --rm --pod economic-pod \
  -v ./backend/migration:/liquibase/changelog:Z \
  liquibase/liquibase:4.25-alpine \
  --url=jdbc:postgresql://localhost:5432/economic_indicators \
  --username=postgres --password=postgres \
  --changeLogFile=changelog/db.changelog-master.xml update

# Start backend
podman run -d --pod economic-pod --name economic-backend \
  -e MSFINTECH_POSTGRES_SERVER=localhost -e MSFINTECH_POSTGRES_PORT=5432 \
  -e MSFINTECH_POSTGRES_USER=postgres -e MSFINTECH_POSTGRES_PASSWORD=postgres \
  -e MSFINTECH_POSTGRES_DB=economic_indicators \
  economic-indicators-api

# Start UI
podman run -d --pod economic-pod --name economic-ui economic-indicators-ui
```

#### Podman Cleanup

```bash
podman pod stop economic-pod
podman pod rm economic-pod
podman system prune -a
```

---

### 3. Local Development Setup

#### Step 1: Setup Database

```bash
# Create database (via psql or pgAdmin)
psql -U postgres -c "CREATE DATABASE economic_indicators;"
```

#### Step 2: Run Liquibase Migrations

**Using Docker:**
```bash
cd backend
docker run --rm --network host \
  -v "$(pwd)/migration:/liquibase/changelog" \
  liquibase/liquibase:4.25-alpine \
  --url=jdbc:postgresql://localhost:5432/economic_indicators \
  --username=postgres --password=postgres \
  --changeLogFile=changelog/db.changelog-master.xml update
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
# Get Podman VM gateway IP
podman machine ssh "ip route | grep default"
# Example output: default via 172.31.224.1

# Run with host IP
podman run --rm \
  -v "c:\path\to\backend\migration:/liquibase/changelog:Z" \
  liquibase/liquibase:4.25-alpine \
  --url=jdbc:postgresql://172.31.224.1:5432/economic_indicators \
  --username=postgres --password=postgres \
  --changeLogFile=changelog/db.changelog-master.xml update
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
$env:MSFINTECH_POSTGRES_SERVER="127.0.0.1"
$env:MSFINTECH_POSTGRES_PORT="5432"
$env:MSFINTECH_POSTGRES_USER="postgres"
$env:MSFINTECH_POSTGRES_PASSWORD="postgres"
$env:MSFINTECH_POSTGRES_DB="economic_indicators"
$env:PYTHONPATH=(Get-Location).Path

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Linux/macOS:**
```bash
cd backend
export MSFINTECH_POSTGRES_SERVER=127.0.0.1
export MSFINTECH_POSTGRES_PORT=5432
export MSFINTECH_POSTGRES_USER=postgres
export MSFINTECH_POSTGRES_PASSWORD=postgres
export MSFINTECH_POSTGRES_DB=economic_indicators
export PYTHONPATH=$(pwd)

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 4: Start Frontend

```bash
cd ui
npm install
npm run dev
```

**Access:** http://localhost:3000 (proxies API to :8000)

---

### 4. Production Linux Server

#### Install Dependencies

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx
```

#### Deploy Application

```bash
git clone <repository-url>
cd msfintech
docker compose up -d
```

#### Configure Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/economic-dashboard
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/economic-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### 5. Azure Deployment

```bash
# Login
az login

# Create resources
az group create --name economic-rg --location eastus
az acr create --resource-group economic-rg --name economicacr --sku Basic

# Build and push images
az acr build --registry economicacr --image economic-api:v1 ./backend
az acr build --registry economicacr --image economic-ui:v1 ./ui

# Deploy to Container Apps
az containerapp create \
  --name economic-api \
  --resource-group economic-rg \
  --image economicacr.azurecr.io/economic-api:v1 \
  --target-port 8000 \
  --ingress external
```

---

## Configuration

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MSFINTECH_POSTGRES_SERVER` | Database host | `127.0.0.1` |
| `MSFINTECH_POSTGRES_PORT` | Database port | `5432` |
| `MSFINTECH_POSTGRES_USER` | Database user | `postgres` |
| `MSFINTECH_POSTGRES_PASSWORD` | Database password | `postgres` |
| `MSFINTECH_POSTGRES_DB` | Database name | `economic_indicators` |

The database password is different from the app login password. PostgreSQL uses `postgres`; the seeded app user uses `all4one`.

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | API base URL | `/api/v1` |

---

## API Reference

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health |
| GET | `/` | Welcome message |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/auth/register` | Register user |
| GET | `/api/v1/auth/me` | Get current user |

### Example: Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "msadmin", "password": "all4one"}'
```

**Response:**
```json
{
  "id": 1,
  "username": "msadmin",
  "email": "msadmin@economic-dashboard.com",
  "full_name": "MS Admin",
  "is_active": true,
  "created_at": "2026-06-26T00:00:00",
  "updated_at": "2026-06-26T00:00:00"
}
```

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/api/v1/auth/users/{user_id}` | Update user full name and password |
| DELETE | `/api/v1/auth/users/{user_id}` | Deactivate user by setting `is_active` to false |

Protected user management APIs use HTTP Basic Authentication in Swagger. Click **Authorize** and enter the app credentials:

| Username | Password |
|----------|----------|
| `msadmin` | `all4one` |

The update API only accepts `full_name` and `password`. It does not update username, email, created date, or active status. The modification date is stored in `updated_at`.

The delete API is a soft delete. It does not remove the user row from PostgreSQL. It sets `is_active` to `false` and updates `updated_at` so the record stays available for future reference.

---

## Roles and Access Control

The project should use roles to define what a user is allowed to do after their username and password are verified.

Recommended roles:

| Role | Purpose |
|------|---------|
| `admin` | Full access to user management, role management, and protected APIs |
| `analyst` | Access to dashboard and economic data features |
| `inactive` | No active access; used for users who are deactivated but kept for future reference |

Protected role and user-management APIs should use HTTP Basic Authentication in Swagger. Click **Authorize** and enter:

| Username | Password |
|----------|----------|
| `msadmin` | `all4one` |

Swagger sends the credentials as a Basic Auth header:

```http
Authorization: Basic ...
```

No JWT token, Bearer token, or `access_token` is required.

Basic Authentication confirms that the username and password are valid. Role checks should then decide whether the authenticated user is allowed to perform the action. For example, creating roles should be limited to users with the `admin` role.

Suggested role APIs:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/roles` | Create a role |
| GET | `/api/v1/roles` | List roles |

When roles are added, each user should store a `role_id`. A normal active user can have the `admin` or `analyst` role. A deactivated user should have:

```text
is_active = false
role = inactive
```

This keeps deleted users in PostgreSQL for future reference while preventing them from accessing protected APIs.

## Troubleshooting

If Liquibase reports duplicate changelog file warnings, use the compose commands in this repo. They mount `backend/migration/changelog` directly at `/liquibase/changelog` and use `--changeLogFile=db.changelog-master.xml`.

If the backend starts before tables exist, rebuild and start through compose:

```bash
cd backend
docker compose up -d --build
```

### Test Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "msadmin", "password": "all4one"}'
```

### Test UI

Open http://localhost:3000 (dev) or http://localhost:8081 (production)

---

## Component Documentation

- [Backend README](backend/README.md) - FastAPI service details
- [UI README](ui/README.md) - React frontend details

---

## License

MIT License

---

## Support

For issues and questions, please open a GitHub issue.
=======
# msfintech
>>>>>>> other-repo/main
