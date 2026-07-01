<<<<<<< HEAD
# Economic Indicators Dashboard

A full-stack economic intelligence platform for tracking macroeconomic indicators and financial market data.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [API Reference](#api-reference)
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
├── backend/                    # FastAPI Backend
│   ├── app/                    # Application code
│   │   ├── api/v1/endpoints/   # REST endpoints
│   │   ├── core/               # Config, security
│   │   ├── db/                 # Database setup
│   │   ├── models/             # SQLAlchemy models
│   │   └── schemas/            # Pydantic schemas
│   ├── migration/              # Liquibase migrations
│   ├── Dockerfile
│   └── requirements.txt
├── ui/                         # React Frontend
│   ├── src/
│   │   ├── features/           # Login, Dashboard
│   │   └── shared/             # Services, contexts
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml          # Full stack deployment
└── README.md
```

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend build |
| PostgreSQL | 16+ | Database |

### Container Runtime (Choose One)

| Option | Installation |
|--------|--------------|
| Docker | https://docs.docker.com/get-docker/ |
| Podman | `winget install RedHat.Podman` (Windows) |

---

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone and deploy
git clone <repository-url>
cd msfintech
docker compose up -d

# Verify services
docker compose ps
```

**Access URLs:**

| Service | URL |
|---------|-----|
| UI | http://localhost:8081 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

### Option 2: Podman Compose

```bash
cd msfintech
podman-compose up -d
```

### Option 3: Local Development

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

**Using Podman (Windows - requires host IP):**
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

> **Note:** On Windows with Podman, you may need to add pg_hba.conf entry:
> ```
> host all all 172.31.0.0/16 scram-sha-256
> ```
> Then restart PostgreSQL service.

#### Step 3: Start Backend

**Windows PowerShell:**
```powershell
cd backend
$env:MSFINTECH_POSTGRES_SERVER="127.0.0.1"
$env:MSFINTECH_POSTGRES_PORT="5432"
$env:MSFINTECH_POSTGRES_USER="postgres"
$env:MSFINTECH_POSTGRES_PASSWORD="postgres"
$env:MSFINTECH_POSTGRES_DB="economic_indicators"
$env:PYTHONPATH=(Get-Location).Path

pip install -r requirements.txt
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

## Troubleshooting

### Database Connection Failed

**Error:** `connection to server failed: password authentication failed`

**Solution:**
1. Verify PostgreSQL is running: `Get-Service postgresql*` (Windows) or `systemctl status postgresql`
2. Check password in environment variables matches database
3. For Podman, ensure pg_hba.conf allows container network

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Set PYTHONPATH to backend directory:
```bash
export PYTHONPATH=/path/to/backend  # Linux/Mac
$env:PYTHONPATH="C:\path\to\backend"  # Windows
```

### Liquibase Connection Refused (Podman)

**Error:** `Connection refused` when running Liquibase in Podman

**Solution:** Use host machine IP instead of `localhost`:
```bash
# Get gateway IP
podman machine ssh "ip route | grep default"
# Use that IP in JDBC URL
```

### UI Cannot Connect to API

**Error:** Network error or CORS error

**Solution:**
- Development: Ensure backend is running on port 8000
- Production: Check nginx proxy configuration

---

## Testing

### Test API Health

```bash
curl http://localhost:8000/health
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
>>>>>>> 4005e2e44a90bfeeb340117b7678b2ccb1ede9f1
