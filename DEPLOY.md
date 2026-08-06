# Deploying CyberVerse AI

The app ships as a single Docker image: FastAPI serves both the API
(`/api/*`) and the frontend (everything else) from one process, backed by
Postgres. This is deliberately simple - one container, one database,
no separate frontend host/CDN needed to get a real deployment live.

## 0. Before you deploy — checklist

- [ ] A real `ANTHROPIC_API_KEY` from https://console.anthropic.com/settings/keys
- [ ] A generated `JWT_SECRET`: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- [ ] A domain (or you'll use the platform's generated subdomain)
- [ ] SMTP credentials if you want password-reset emails to actually send
      (any provider works: Postmark, SendGrid SMTP, AWS SES SMTP, even a
      Gmail app password for testing). Without this, reset links just get
      logged to your container logs — nobody receives them.

## Option A — Docker Compose on a VPS (DigitalOcean, Hetzner, EC2, etc.)

This is the most direct path: one small VM, Docker, done.

```bash
# On the server
git clone <your-repo-url> cyberverse && cd cyberverse
cp .env.example .env
nano .env   # fill in JWT_SECRET, ANTHROPIC_API_KEY, POSTGRES_PASSWORD, etc.

docker compose up -d --build
docker compose logs -f app   # watch it come up; alembic upgrade runs automatically
```

The app is now listening on port 8000. Put a reverse proxy in front of it
for HTTPS and your real domain — the simplest option is
[Caddy](https://caddyserver.com/), which gets you free auto-renewing TLS
with a two-line config:

```
# /etc/caddy/Caddyfile
app.yourdomain.com {
    reverse_proxy localhost:8000
}
```

```bash
sudo apt install caddy
sudo systemctl restart caddy
```

Set `APP_BASE_URL=https://app.yourdomain.com` in `.env` and restart
(`docker compose up -d`) so password-reset emails link to the right place.

**Updating**: `git pull && docker compose up -d --build` — migrations run
automatically on container start.

## Option B — Render / Railway / Fly.io (managed, no server to babysit)

All three can build directly from the root `Dockerfile`.

1. Create a **Postgres** database on the platform — copy its connection
   string into `DATABASE_URL`.
2. Create a **web service** pointing at this repo, build type "Docker",
   no build/start command overrides needed (the `Dockerfile` CMD handles
   migrations + gunicorn startup).
3. Set environment variables: `JWT_SECRET`, `ANTHROPIC_API_KEY`,
   `DATABASE_URL`, `APP_BASE_URL` (the URL the platform gives your service),
   `ENVIRONMENT=production`, and SMTP_* if you want real emails.
4. Deploy. First boot runs `alembic upgrade head` automatically.

Render/Railway both give you a free `*.onrender.com` / `*.up.railway.app`
HTTPS domain immediately — good enough to launch on before you point a real
domain at it.

## Option C — Split deployment (frontend on a CDN, backend elsewhere)

If you'd rather put the frontend on Vercel/Netlify/Cloudflare Pages and the
backend somewhere else:

1. Deploy `backend/` alone (same Dockerfile works, or just `pip install -r
   requirements.txt && alembic upgrade head && gunicorn ...`).
2. Set `FRONTEND_DIR=` (empty) so FastAPI doesn't try to serve static files.
3. Set `ALLOWED_ORIGINS` to your frontend's real domain.
4. In `frontend/app.js`, change the `API_BASE` constant to hardcode your
   backend's URL instead of relying on the localhost/same-origin heuristic.
5. Deploy `frontend/` as static files (it's plain HTML/CSS/JS — any static
   host works, no build step).

This adds operational overhead (two things to deploy, CORS to manage) for
no real benefit at this scale — Option A or B is recommended unless you have
a specific reason to split them (e.g. a CDN you already run everything else
through).

## Database migrations going forward

Never edit tables by hand. When you change `models.py`:

```bash
cd backend
alembic revision --autogenerate -m "describe the change"
# review the generated file in alembic/versions/ - autogenerate isn't perfect
alembic upgrade head          # apply locally to test
git add alembic/versions/*.py && git commit
```

The Docker image runs `alembic upgrade head` on every container start, so
committed migrations apply automatically on deploy.

## Monitoring what it's costing you

Every AI Mentor / Daily Ops / Resume Review / Interview Coach call hits the
Anthropic API and costs money. The rate limits in `.env`
(`RATE_LIMIT_CHAT`, etc.) are a blunt cap on abuse, not a cost dashboard —
watch actual spend at https://console.anthropic.com/settings/usage and
tighten the limits (or add per-plan limits once you have paid tiers) if
usage looks off.

## What's still missing for a full commercial launch

This gets you a real, secure, deployable product for Phase 1 of the vision
doc. Not yet built, in rough priority order:

1. **Payments** — Razorpay/Stripe integration for the Pro/Premium/Enterprise
   tiers and gating features by plan.
2. **Email verification** — accounts currently work unverified; add if you
   see signup abuse.
3. **Object storage** — resumes are stored as text in Postgres; fine for
   MVP scale, move to S3/R2 if you start storing original files.
4. **Phase 2/3 features** — hands-on labs, GRC workspace, employer portal,
   marketplace — genuinely separate subsystems, build as new FastAPI routers
   + new frontend views when you get there.
