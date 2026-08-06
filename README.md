# CyberVerse AI

Phase 1 of the CyberVerse AI vision doc, built as a real, deployable product:
**AI Mentor, Learning Paths, Daily Learning, AI Resume Builder, and Interview
Coach.** Production-hardened — Postgres + migrations, password reset, rate
limiting, file uploads, automated tests, CI, and a one-command Docker deploy.

👉 **Deploying?** See [`DEPLOY.md`](./DEPLOY.md) for step-by-step instructions.

## What's built

**Backend** (`/backend` — FastAPI + Postgres/SQLite + JWT), AI-powered by the
Anthropic Claude API:
- `POST /api/mentor/chat` — AI Mentor with persistent per-user memory (skill
  level, certifications, weak topics, goals) injected into every
  conversation, plus rolling chat history.
- `GET /api/daily` — generates and caches one daily bundle: lesson, quiz,
  news summary, challenge, interview question, practical task. Drives the
  XP/streak counters.
- `POST /api/resume/review` / `POST /api/resume/review-upload` — scores a
  resume (pasted text or an uploaded `.pdf`/`.docx`/`.txt`), flags ATS
  issues and skill gaps, rewrites weak bullets.
- `POST /api/interview/start` + `POST /api/interview/{id}/respond` — a
  multi-turn simulated interview with per-answer feedback and a final score.
- `GET/PATCH /api/profile/me` — the memory the AI Mentor draws on.
- `POST /api/auth/{signup,login,forgot-password,reset-password}` — full auth
  including a real password-reset flow (emailed via SMTP, or logged to
  console in dev).

**Production hardening:**
- **Postgres in production, SQLite for local dev** — same code, just change
  `DATABASE_URL`.
- **Alembic migrations** — schema changes are tracked and applied on deploy,
  not implicit `create_all()` calls.
- **Rate limiting** on every AI-backed endpoint and all auth endpoints
  (configurable per-route in `.env`), since AI calls cost real money.
- **CORS locked to explicit origins**, security headers on every response.
- **Automated tests** (19 tests, Claude API calls mocked) covering auth,
  password reset, profile memory, and every AI feature — runs in CI on every
  push (`.github/workflows/ci.yml`).
- **Docker**: one image serves both the API and the static frontend from a
  single origin, with `gunicorn` + Uvicorn workers, a healthcheck, and
  migrations run automatically on container start.

**Frontend** (`/frontend`) — a single-page vanilla HTML/CSS/JS app (no build
step): Dashboard, AI Mentor chat, Daily Ops, Resume Builder (paste or
upload), Interview Coach, Profile, plus forgot/reset password. Styled as a
SOC console rather than a generic SaaS template.

Not built yet (Phase 2/3 in the vision doc): hands-on browser labs, GRC
workspace, employer/jobs portal, marketplace, payments. See the bottom of
`DEPLOY.md` for what's next.

## Run it locally

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt   # includes pytest

cp .env.example .env
# edit .env: set ANTHROPIC_API_KEY (required), everything else has a
# working default for local dev (SQLite, console-logged emails, etc.)

alembic upgrade head        # creates the local SQLite schema
uvicorn main:app --reload --port 8000
```

Open `http://127.0.0.1:8000` — FastAPI serves the frontend directly, same as
it will in production. (You can also run the frontend on its own dev server
with `cd frontend && python3 -m http.server 8080` if you prefer; `app.js`
auto-detects localhost and points at `http://127.0.0.1:8000` for the API.)

Interactive API docs: `http://127.0.0.1:8000/docs`.

### Run the tests

```bash
cd backend
pytest -v
```

All AI-backed tests mock the Claude API, so no API key or network access is
needed to run the suite.

### Try it

1. Create an account.
2. Go to **Profile**, set a skill level, a certification, a weak topic, and
   a goal — this is what the AI Mentor remembers about you.
3. **AI Mentor** → ask "Explain SQL Injection like I'm 10" and notice the
   answer is pitched to the skill level you just set.
4. Try **Daily Ops**, **Resume Builder** (paste text or upload a file), and
   **Interview Coach**.
5. Log out, click **Forgot your password?**, then check your terminal — the
   reset link is logged there unless you've configured SMTP.

## Deploying for real

Full instructions, including a one-command Docker Compose setup with
Postgres and HTTPS via Caddy, are in [`DEPLOY.md`](./DEPLOY.md).

Quick version:

```bash
cp .env.example .env   # fill in JWT_SECRET, ANTHROPIC_API_KEY, POSTGRES_PASSWORD
docker compose up -d --build
```

## Notes on the AI backend choice

Everything routes through `backend/claude_client.py`, which calls the
Anthropic `/v1/messages` API directly. This was chosen over OpenAI because
the mentor/coach/interviewer personas all lean on careful system-prompt
instruction-following, which Claude models are strong at, and because
you're already in the Claude ecosystem. If you'd rather use OpenAI or a
local model, only `claude_client.py` needs to change — every route calls
`call_claude()` / `call_claude_json()`, so the rest of the app is
provider-agnostic.
