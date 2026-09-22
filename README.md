# devboard-core

**The user profiles.** It stores who each user is: username, avatar, timezone, role and status. Other services ask it about users.

- **Port:** `8003`
- **Stack:** Django, Django REST Framework (async views), PostgreSQL

---

## Start here (about 5 minutes)

1. Open a terminal in `devboard-infra`.
2. Run `setup.bat`. It creates the database, starts this service and runs the migrations.
3. Open `http://localhost:8003/api/users/me/`. It answers `401`, which means the service is up and wants a login.

Only want this one service? The database must already be running. Then:

```bash
docker compose up --build -d
docker compose exec devboard-core python manage.py migrate
```

---

## What it does

1. **Creates a profile** when a user signs up (devboard-auth calls it).
2. **Shows and edits your profile** (avatar and timezone).
3. **Lets admins** list users, deactivate them and change their role.
4. **Answers other services**: find users by id, username or email.

---

## How it fits

```
devboard-auth ──sync after sign-up──> devboard-core
devboard-core ──role / status change──> devboard-auth
devboard-work ──find users by name or email──> devboard-core
```

- devboard-auth owns the **login**. devboard-core owns the **profile**.
- Both keep a role and a status. When an admin changes one here, core tells devboard-auth. If auth is unreachable, the change fails with `502` and nothing is saved.

---

## Who can do what

| Caller | How it proves itself | Can do |
|---|---|---|
| Normal user | `Authorization: Bearer <jwt>` | Own profile, look up other users. |
| Admin | Bearer token with role `admin` in core | Everything above, plus list users, change status and role. |
| Another service | `X-Service-Key: <INTERNAL_API_KEY>` | Sync users and look them up. |

Inactive users are blocked even with a valid token. Each request also updates the user's `last_active` time.

---

## API

Base path: `/api/users/`

### User routes (Bearer)

| Method | Path | What it does |
|---|---|---|
| `GET` | `/me/` | Your profile. |
| `PATCH` | `/me/` | Change your `avatar` or `timezone`. |
| `GET` | `/<user_id>/` | Public info: id, username, avatar. |
| `POST` | `/batch/` | Public info for up to 100 ids. Body: `{"ids": [...]}`. |

### Admin routes (Bearer + admin)

| Method | Path | What it does |
|---|---|---|
| `GET` | `/` | List all users. Uses `limit` and `offset`. |
| `PATCH` | `/<user_id>/status/` | Set `active` or `inactive`. |
| `PATCH` | `/<user_id>/role/` | Set `admin` or `member`. |

### Service routes (`X-Service-Key`)

| Method | Path | What it does |
|---|---|---|
| `POST` | `/sync/` | Create or update a profile. Called by devboard-auth. |
| `GET` | `/search/?email=...` | Find a user by email. |
| `POST` | `/lookup/` | Find users by username (max 25). Body: `{"usernames": [...]}`. |
| `GET` | `/internal/<user_id>/status/` | Get a user's status. |

---

## Settings

Copy `.env.example` to `.env`.

| Variable | What it is |
|---|---|
| `SECRET_KEY` | Django secret key. |
| `DEBUG` | `True` or `False`. |
| `DB_NAME` `DB_USER` `DB_PASSWORD` | Database login. |
| `DB_HOST` `DB_PORT` | Database address. Docker overrides them. |
| `JWT_SECRET` | Same value as devboard-auth. Used to check tokens. |
| `INTERNAL_API_KEY` | Shared key for service-to-service calls. |
| `AUTH_SERVICE_URL` | Where devboard-auth lives. |

---

## Data

One table: `user_profiles`.

| Field | Notes |
|---|---|
| `user_id` | Same id as in devboard-auth. |
| `email`, `username` | Both unique. |
| `avatar`, `timezone` | The user can edit these. Default timezone: `Europe/Bucharest`. |
| `role` | `admin` or `member`. |
| `status` | `active` or `inactive`. |
| `last_active`, `created_at`, `updated_at` | Set by the service. |

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Good to know

- **Email, username and role cannot be edited** through `PATCH /me/`.
- **No bind mount in Docker.** After a code change, rebuild the image.
