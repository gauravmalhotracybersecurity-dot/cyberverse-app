# CyberVerse AI - Frontend Specification Document

## 4.1 Pages
| Route | Purpose |
|---|---|
| / | Marketing landing (hero, loop explainer, features, pricing, CTAs) |
| /app.html | Auth screen + app shell (all product views) |
| /admin.html | Founder console (stats, charts, signups) |

## 4.2 Design System
- Theme: dark-only. BG #0a0a0a, surfaces #151515, borders #222.
- Accent: neon teal #00ffcc; Pro: gold-orange gradient #f5af19 to #f12711.
- Type: Inter (UI) + IBM Plex Mono / Consolas (brand, labels, code).
- Components: nav-item, status-bar, cards, chat-shell, modal-overlay (paywall, scorecard), badges (pro-badge), primary/secondary buttons.

## 4.3 View Map (/app.html)
view-dashboard (snapshot + learning paths); view-mentor (chat); view-daily (bundle); view-resume (form + review); view-interview (setup vs session, interview-new button); view-achievements; view-profile. Modals: paywall-modal, scorecard-modal.

## 4.4 State and Client Behavior
- Token: localStorage cv_token; profile in-memory per session.
- API_BASE: same-origin in prod; http://127.0.0.1:8000 on localhost.
- Boot: token -> enterApp(); 401 -> clean logout state.
- Navigation: goToView(); interview view auto-checks GET /api/interview/active.
- Scorecard: client-side canvas render 1080x1350 PNG + clipboard LinkedIn post.

## 4.5 Key Flows
1. Auth: login/signup JSON -> access_token -> shell.
2. Interview: start -> 6 turns -> completion -> score modal -> share.
3. Paywall: free-limit hit -> modal -> Razorpay link -> webhook flips entitlement -> UI hides CTA, shows PRO badge.

## 4.6 Quality Requirements
Responsive (landing done; app shell mobile nav = debt); A11y focus states + aria labels (debt); vanilla JS, edits must stay idempotent and null-safe.
