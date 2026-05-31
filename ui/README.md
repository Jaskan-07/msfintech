# Economic Indicators Dashboard - UI

React frontend with TypeScript, Vite, and JWT authentication.

> **Full deployment instructions:** See [Root README](../README.md)

---

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development](#development)
- [Configuration](#configuration)
- [Pages](#pages)
- [API Integration](#api-integration)
- [Docker](#docker)
- [Troubleshooting](#troubleshooting)

---

## Project Structure

```
ui/
├── src/
│   ├── main.tsx                    # Entry point
│   ├── app/
│   │   └── App.tsx                 # Root component, routing
│   ├── features/
│   │   ├── auth/
│   │   │   ├── Login.tsx           # Login page
│   │   │   └── Login.css
│   │   └── dashboard/
│   │       ├── Dashboard.tsx       # Dashboard page
│   │       └── Dashboard.css
│   ├── shared/
│   │   ├── components/
│   │   │   └── ProtectedRoute.tsx  # Auth guard
│   │   ├── context/
│   │   │   └── AuthContext.tsx     # Auth state
│   │   └── services/
│   │       └── authService.ts      # Auth API calls
│   ├── config/
│   │   └── api.ts                  # API configuration
│   └── styles/
│       └── index.css
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── Dockerfile
├── nginx.conf
└── README.md
```

---

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Node.js | 18+ | Runtime |
| npm | 9+ | Package manager |

---

## Quick Start

```bash
cd ui
npm install
npm run dev
```

**Access:** http://localhost:3000

---

## Development

### Install Dependencies

```bash
npm install
```

### Start Development Server

```bash
npm run dev
```

The app runs at http://localhost:3000 with hot reload enabled.

> **API Proxy:** Development server proxies `/api` requests to `http://localhost:8000`

### Build for Production

```bash
npm run build
```

Output: `dist/` folder

### Preview Production Build

```bash
npm run preview
```

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (port 3000) |
| `npm run build` | Production build |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

---

## Configuration

### Environment Variables

Create `.env` file:

```bash
VITE_API_URL=/api/v1
```

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `/api/v1` |

### Vite Proxy Configuration

Development proxy is configured in `vite.config.ts`:

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

---

## Pages

### Login (`/login`)

| Feature | Description |
|---------|-------------|
| Username/Password form | Standard auth fields |
| Error handling | Shows error messages |
| Loading state | Disables button during request |
| Redirect | Goes to dashboard on success |

### Dashboard (`/dashboard`)

| Feature | Description |
|---------|-------------|
| Protected route | Requires authentication |
| Logout button | Clears token, redirects to login |
| Placeholder | For economic indicators |

### Default Credentials

| Username | Password |
|----------|----------|
| `msadmin` | `all4one` |

---

## API Integration

### Auth Service

Located at `src/shared/services/authService.ts`:

| Function | Description |
|----------|-------------|
| `login(username, password)` | POST to `/api/v1/auth/login` |
| `register(data)` | POST to `/api/v1/auth/register` |
| `getToken()` | Get token from localStorage |
| `setToken(token)` | Save token to localStorage |
| `removeToken()` | Clear token from localStorage |

### Auth Context

Located at `src/shared/context/AuthContext.tsx`:

| Property/Method | Description |
|-----------------|-------------|
| `isAuthenticated` | Boolean auth status |
| `token` | Current JWT token |
| `login(username, password)` | Authenticate user |
| `logout()` | Clear auth state |

### API Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/auth/register` | POST | User registration |
| `/api/v1/auth/me` | GET | Get user info |

### Example Login Request

```typescript
const response = await axios.post('/api/v1/auth/login', {
  username: 'msadmin',
  password: 'all4one'
});
// Returns: { access_token: '...', token_type: 'bearer' }
```

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type Safety |
| Vite | 5.x | Build Tool |
| React Router | 6.x | Routing |
| Axios | Latest | HTTP Client |

---

## Docker

### Build Image

```bash
docker build -t economic-indicators-ui .
```

### Run Container

```bash
docker run -d -p 8081:8081 --name economic-ui economic-indicators-ui
```

**Access:** http://localhost:8081

### Nginx Configuration

Production uses Nginx (`nginx.conf`):
- Serves static files from `/usr/share/nginx/html`
- Proxies `/api` to backend service
- Handles React Router (SPA fallback)

---

## Podman

### Build Image

```bash
podman build -t economic-indicators-ui .
```

### Run Container

```bash
podman run -d -p 8081:8081 --name economic-ui economic-indicators-ui
```

### Cleanup

```bash
podman stop economic-ui
podman rm economic-ui
podman rmi economic-indicators-ui
```

---

## Troubleshooting

### API Connection Error

**Problem:** Login fails with network error

**Solutions:**
1. Ensure backend is running on port 8000
2. Check Vite proxy configuration
3. Verify API URL in environment

```bash
# Start backend
cd ../backend
python -m uvicorn app.main:app --port 8000
```

### CORS Error

**Problem:** CORS policy blocks requests

**Solutions:**
- Development: Vite proxy handles CORS
- Production: Nginx proxies API requests

### Build Fails

**Problem:** TypeScript errors

**Solutions:**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install

# Check for type errors
npm run lint
```

### Blank Page After Build

**Problem:** Production build shows blank page

**Solutions:**
1. Check browser console for errors
2. Verify base URL in `vite.config.ts`
3. Ensure nginx serves index.html for all routes

---

## File Reference

| File | Purpose |
|------|---------|
| `src/main.tsx` | Application entry point |
| `src/app/App.tsx` | Root component with routing |
| `src/features/auth/Login.tsx` | Login page component |
| `src/shared/context/AuthContext.tsx` | Authentication state |
| `src/shared/services/authService.ts` | API authentication calls |
| `src/shared/components/ProtectedRoute.tsx` | Route guard |
| `vite.config.ts` | Vite configuration with proxy |
| `nginx.conf` | Production Nginx config |
| `Dockerfile` | Multi-stage Docker build |

---

## License

MIT License