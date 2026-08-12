# devboard-core

Core microservice for the Devboard platform. Handles user profiles, role management, and status changes.

## Stack

- **Django** — web framework
- **Django REST Framework** — API layer
- **PostgreSQL** — database
- **python-jose** — JWT decoding
- **httpx** — communicates with devboard-auth
- **whitenoise** — static file serving

## Environment Variables

Copy `.env.example` to `.env` and fill in the values.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (`True`/`False`) |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host (default: `localhost`) |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `INTERNAL_API_KEY` | Shared secret key for internal service calls |
| `JWT_SECRET` | Secret key for verifying JWTs issued by devboard-auth |
| `AUTH_SERVICE_URL` | URL of the devboard-auth service |

## Running with Docker

```bash
docker compose up --build -d
docker compose exec devboard-core python manage.py migrate
docker compose down
```

## API

Base path: `/api/users`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/users/sync/` | `X-Service-Key` | Sync user from devboard-auth (internal) |
| `GET` | `/api/users/me/` | Bearer | Get current user profile |
| `PATCH` | `/api/users/me/` | Bearer | Update current user profile |
| `PATCH` | `/api/users/<user_id>/status/` | Bearer (admin) | Activate or deactivate a user |

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
