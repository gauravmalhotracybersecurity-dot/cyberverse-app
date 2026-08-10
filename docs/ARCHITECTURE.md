# CyberVerse AI - Technical Architecture Document

## 2.1 High-Level Diagram


## 2.2 Data Model (key columns)
| Table | Key columns |
|---|---|
| users | email, hashed_password, full_name, skill_level, certifications[], weak_topics[], learning_goals, xp, streak_days, last_active_date, is_pro, is_premium, created_at |
| mentor_messages | user_id, role, content |
| daily_bundles | user_id, date, content(JSON) |
| resume_reviews | user_id, role, review(JSON) |
| interview_sessions | user_id, role, status(active/completed), overall_score |
| interview_turns | session_id, speaker, content, feedback |
| achievements | user_id, type, title, date |

## 2.3 API Surface (principal endpoints)
| Method | Path | Purpose |
|---|---|---|
| POST | /api/auth/signup, /login, /forgot-password, /reset-password | Auth |
| GET | /api/profile/me | Profile incl. is_pro |
| POST | /api/mentor/chat | Context-aware mentor |
| GET | /api/daily/today | Daily bundle |
| POST | /api/resume/review | Resume analysis |
| POST | /api/interview/start, /{id}/respond | Interview lifecycle |
| GET | /api/interview/active | Session resume |
| POST | /api/webhooks/razorpay | HMAC-verified upgrade |
| GET | /api/admin/stats | Founder metrics (allowlist) |

## 2.4 Deployment and Ops
GitHub push -> Render build -> Alembic migrations -> idempotent runtime ALTER safety net -> Gunicorn serve. Config via pydantic-settings.

## 2.5 Environment Variables
DATABASE_URL, JWT_SECRET, ANTHROPIC_API_KEY, RESEND_API_KEY, RESEND_FROM_EMAIL, RAZORPAY_WEBHOOK_SECRET, ADMIN_EMAIL(S), APP_BASE_URL, RATE_LIMIT_*

## 2.6 Scaling Path
Stateless API -> horizontal workers; extract cron to external scheduler/queue; Redis for rate-limit + cache; S3/R2 for resume files; CDN for static assets; read replicas when needed.
