# CyberVerse AI - Feature Ticket List

## Shipped (record)
AUTH-1 JWT auth + reset; MEN-1 mentor; DLY-1 daily ops + cron email; RES-1 resume review; INT-1..5 interviews, resume-session, memory, score; GAM-1 XP/streaks/achievements; PAY-1..3 gate, paywall, webhook upgrade; GRW-1..4 landing, welcome email, scorecard share, founder console.

## Backlog
| ID | Title | Description | Pri | Size |
|---|---|---|---|---|
| CV-104 | Parse verdict text into scorecard | Fill empty verdict line from closing remarks | P0 | S |
| CV-105 | Sanitize AI-rendered HTML (XSS) | Escape/DOMPurify all AI + user content | P0 | M |
| CV-126 | Fix password-reset deep link | Point to /app.html?reset_token= + handler | P0 | S |
| CV-101 | Programmatic SEO question pages | /questions/* pages funneling to signup | P1 | L |
| CV-102 | Resume review share card | Second viral loop (resume score PNG) | P1 | M |
| CV-103 | Referral engine | +1 free interview both sides | P1 | M |
| CV-110 | Premium tier Rs 999 | Amount-based webhook tiering + UI | P1 | M |
| CV-111 | PDF certificates (reportlab) | Premium perk on completed interviews | P1 | M |
| CV-121 | Abandoned-interview nudge email | Lift start-to-completion rate | P1 | S |
| CV-123 | Mobile app shell + bottom nav | Responsive product views | P1 | M |
| CV-135 | Terms and Privacy pages | Legal baseline for payments | P1 | S |
| CV-120 | Day-3/Day-7 nurture emails | Retention drip | P2 | S |
| CV-122 | Skill radar chart | Visual weak-topic radar on dashboard | P2 | M |
| CV-124 | Toast system | Replace alerts | P2 | S |
| CV-130 | Signup email verification | Anti-abuse | P2 | M |
| CV-131 | External cron for daily email | Off-process scheduler | P2 | M |
| CV-132 | Redis rate-limit + cache | Scale control plane | P2 | M |
| CV-133 | S3/R2 resume storage | Persist uploads | P2 | M |
| CV-134 | Audit log | Admin + webhook events | P2 | S |
| CV-201 | Labs architecture spike | Containers/WebSockets feasibility | P3 | L |
| CV-202 | GRC workspace MVP | Risk register, assets, evidence (B2B) | P3 | XL |
| CV-203 | Jobs board MVP | Postings + candidate profiles | P3 | L |
| CV-204 | Marketplace MVP | Expert templates/courses w/ commission | P3 | XL |
| CV-205 | Mobile (PWA/Flutter spike) | App-store path | P3 | L |

## Sprint suggestion
P0 trio (CV-104/105/126) -> CV-101 + CV-102 (growth) -> CV-110/111 (revenue).
