from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"  # development | production

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    jwt_secret: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 10080  # 7 days
    reset_token_expire_minutes: int = 30

    database_url: str = "sqlite:///./cyberverse.db"

    # Comma-separated list, e.g. "https://app.cyberverse.ai,https://cyberverse.ai"
    # Ignored entirely when the frontend is served from the same origin as the
    # API (the default in the Docker/production setup) - CORS only matters
    # when frontend and backend are on different origins.
    allowed_origins: str = "http://localhost:8080,http://127.0.0.1:8080"

    # Serve the built frontend directly from FastAPI when this path exists.
    # Set to "" to disable (e.g. if a separate static host serves the frontend).
    frontend_dir: str = "../frontend"

    # SMTP for password-reset emails. If smtp_host is blank, emails are just
    # logged to the console instead of sent - fine for local dev, not for prod.
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "no-reply@cyberverse.ai"
    smtp_use_tls: bool = True

    # Public URL of the frontend, used to build links in emails.
    app_base_url: str = "http://127.0.0.1:8080"

    # Rate limits for AI-backed endpoints (each call costs money).
    rate_limit_chat: str = "30/hour"
    rate_limit_daily: str = "10/hour"
    rate_limit_resume: str = "10/hour"
    rate_limit_interview: str = "20/hour"
    rate_limit_auth: str = "10/minute"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
