# CyberVerse AI - Product Requirements Document (PRD)

Product: CyberVerse AI - Learn. Practice. Get Certified. Get Hired.
Stage: MVP live (v1.x) | Owner: Gaurav Malhotra | URL: app.grcwithgaurav.com

## 1.1 Problem
Cybersecurity job seekers study generic curricula while recruiters reject them for unknown, specific gaps. There is no feedback loop between a user's resume, interview performance, and daily study plan.

## 1.2 Positioning
Not a lab platform (no head-on competition with TryHackMe/HTB). An AI-powered personal career mentor accompanying users from beginner to professional.

## 1.3 Target Personas
| Persona | Goal | Key need |
|---|---|---|
| Aspiring SOC Analyst (student/career-changer) | First job | Know what is missing + practice interviews |
| GRC professional | Cert + role growth | ISO 27001/GRC interview prep |
| Early-career Security Engineer | Better job | Targeted skill closure + resume polish |

## 1.4 Core Value Loop (Weak Topics Loop)
Resume review -> AI detects gaps -> gaps stored as Weak Topics -> Daily Ops + Mentor + Interviews personalize to those topics -> performance updates Weak Topics -> repeat.

## 1.5 Shipped Feature Requirements
| # | Story | Acceptance criteria (met) |
|---|---|---|
| R1 | Account: sign up / log in / reset password via email | JWT session; generic reset response (no user enumeration) |
| R2 | AI Mentor chat with persistent context (skill, certs, goals, weak topics) | Context injected per request |
| R3 | Daily Ops bundle (lesson, quiz, news, challenge, interview Q, task) + 7 AM email | Personalized to weak topics; cron delivery |
| R4 | Resume review: score, ATS issues, gaps, rewritten bullets | Gaps merge into Weak Topics |
| R5 | Mock interview: 4 roles, 6 turns, per-turn feedback, score /100 + verdict | Session resume; question memory; shareable scorecard PNG + LinkedIn copy |
| R6 | Gamification: XP, streaks, levels, Achievements Wins Wall | XP on actions; streak on daily activity |
| R7 | Monetization: Free (3 interviews/3 reviews) to Pro Rs 499 lifetime | Paywall modal; Razorpay link; webhook auto-upgrade (HMAC-verified) |
| R8 | Growth: landing page, welcome email, shareable scorecard | Signup to welcome email under 5 s |
| R9 | Founder Console: signups, Pro conversion, engagement metrics | Admin-email allowlist only |

## 1.6 Monetization
- Free: Mentor, Daily Ops, 3 interviews, 3 reviews.
- Pro Rs 499 (lifetime): unlimited interviews/reviews, PRO badge.
- Planned Premium Rs 999: PDF certificates, advanced analytics. Enterprise: later.

## 1.7 Success Metrics (KPIs)
Signups/week; D1/D7 retention; interview start-to-completion rate (top priority); Free-to-Pro conversion (target 5%+); scorecard shares/week; active-today.

## 1.8 Roadmap (Out of Scope now)
Phase 2: browser labs, AI lab assistant, GRC workspace (B2B). Phase 3: jobs portal, marketplace. Near-term: SEO pages, referrals, Premium certs, mobile.
