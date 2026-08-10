from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"  # development | production

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    jwt_secret: str = "dev-secret-change-me"
    razorpay_webhook_secret: str = "dev_secret"
    admin_email: str = "gaurav.malhotra3300@gmail.com"
    access_token_expire_minutes: int = 10080  # 7 days
    reset_token_expire_minutes: int = 30

    database_url: str = "sqlite:///./cyberverse.db"

    allowed_origins: str = "http://localhost:8080,http://127.0.0.1:8080"

    frontend_dir: str = "../frontend"

    resend_api_key: str = ""
    resend_from_email: str = "onboarding@resend.dev"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "no-reply@cyberverse.ai"
    smtp_use_tls: bool = True

    app_base_url: str = "http://127.0.0.1:8080"

    rate_limit_chat: str = "30/hour"
    rate_limit_daily: str = "10/hour"
    rate_limit_resume: str = "10/hour"
    rate_limit_interview: str = "20/hour"
    rate_limit_auth: str = "10/minute"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


settings = Settings()
