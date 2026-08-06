# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Keep Python output unbuffered and don't write .pyc files in the image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production

WORKDIR /app

# System deps needed by psycopg2 (Postgres driver) and pdfplumber (PDF parsing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first so this layer is cached unless requirements change
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the rest of the app. Frontend sits alongside backend so
# FastAPI's StaticFiles mount (frontend_dir=../frontend) finds it.
COPY backend /app/backend
COPY frontend /app/frontend

WORKDIR /app/backend

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health').read()" || exit 1

# Run migrations, then start the app with gunicorn + uvicorn workers.
# Worker count: rule of thumb is (2 x CPU cores) + 1; 4 is a sane default
# for small deployments - tune via WEB_CONCURRENCY at runtime if needed.
CMD alembic upgrade head && \
    gunicorn main:app \
      --worker-class uvicorn.workers.UvicornWorker \
      --workers ${WEB_CONCURRENCY:-4} \
      --bind 0.0.0.0:8000 \
      --access-logfile - \
      --error-logfile -
