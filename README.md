<div align="center">

<br />

```
     ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗     █████╗ ██╗
     ██║██╔═══██╗██╔══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝    ██╔══██╗██║
     ██║██║   ██║██████╔╝██████╔╝██║   ██║██║     ███████╗█████╗      ███████║██║
██   ██║██║   ██║██╔══██╗██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝      ██╔══██║██║
╚█████╔╝╚██████╔╝██████╔╝██║     ╚██████╔╝███████╗███████║███████╗    ██║  ██║██║
 ╚════╝  ╚═════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝
```

### **Intelligent job aggregation platform that scrapes, filters, and delivers curated opportunities directly to your inbox.**

<br />

[![Live](https://img.shields.io/badge/LIVE-ai--job--alert--platform.vercel.app-D2FF00?style=for-the-badge&logo=vercel&logoColor=black)](https://ai-job-alert-platform.vercel.app)
[![Backend](https://img.shields.io/badge/API-Azure_App_Service-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://jobpulse-hghkebgcafc5erda.eastus-01.azurewebsites.net)
[![License](https://img.shields.io/badge/License-MIT-white?style=for-the-badge)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deployments-45+-22c55e?style=for-the-badge&logo=github-actions&logoColor=white)](.github/workflows)

<br />

</div>

---

## Overview

**JobPulse AI** is a full-stack, production-deployed job alert platform that scrapes and aggregates opportunities from multiple sources, filters them by category, and delivers a curated digest to each registered user at the exact time they choose — across 10 specialised categories.

No manual searching. No missed opportunities. Just signal, zero noise.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                            │
│                  React + Vite  ─────►  Vercel CDN                   │
└───────────────────────────┬─────────────────────────────────────────┘
                            │  HTTPS / JSON
┌───────────────────────────▼─────────────────────────────────────────┐
│                      BACKEND  (FastAPI)                             │
│               Azure App Service  ─  East US                        │
│                                                                     │
│   POST /register    ──► Validate ──► Write user to DB              │
│   GET  /users       ──► Read aggregate count from DB               │
│   GET /run-scheduler ──► Triggered by cron ──► Scrape ──► Email     │
└──────────┬────────────────────────────────────┬─────────────────────┘
           │                                    │
    ┌──────▼──────┐                    ┌────────▼────────┐
    │    Neon     │                    │     Resend      │
    │ PostgreSQL  │                    │  Email Delivery │
    │  (Serverless│                    │   (per user,    │
    │   Database) │                    │  scheduled time)│
    └─────────────┘                    └─────────────────┘
           ▲
    ┌──────┴──────┐
    │ cron-job.org│
    │  Scheduler  │
    │ (triggers   │
    │  daily job) │
    └─────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React 18 + Vite | SPA, component architecture |
| **Styling** | Pure CSS-in-JS (no framework) | Custom design system, zero bloat |
| **HTTP Client** | Axios | API calls with timeout + error handling |
| **Backend** | FastAPI (Python) | REST API, async request handling |
| **Database** | Neon PostgreSQL (serverless) | User storage, schema migrations via Alembic |
| **Email** | Resend | Transactional email delivery |
| **Scheduler** | cron-job.org | Daily trigger for alert pipeline |
| **Frontend Hosting** | Vercel | CDN, automatic deploys from `main` |
| **Backend Hosting** | Azure App Service (East US) | Always-on API server |
| **CI/CD** | GitHub Actions | Automated deploy on push |

---

## Features

- **10 Job Categories** — BTech · MTech · MS Research · Life Sciences · Internships · Remote · AI/ML · Cybersecurity · Cloud · Software
- **User-defined delivery time** — alerts arrive at the exact hour and minute the user chooses
- **Duplicate email detection** — backend + frontend both guard against re-registration
- **Fully accessible UI** — ARIA labels, `aria-live` regions, keyboard navigation, `focus-visible` states
- **Production-oriented error handling** — request timeout safeguards, retry-safe flows, and graceful network failure handling
- **Zero spam architecture** — one digest per user per day, no marketing, no upsells
- **Responsive** — works on mobile, tablet, and desktop without a CSS framework

---

## Project Structure

```
AI-Job-Alert-Platform/
│
├── frontend/                   # React + Vite application
│   ├── src/
│   │   ├── App.jsx             # Main component (all UI + state)
│   │   └── api.js              # Axios instance → Azure backend
│   ├── public/
│   │   └── favicon.ico
│   ├── .env                    # VITE_API_BASE_URL (local)
│   └── vite.config.js
│
├── backend/                    # FastAPI application
│   ├── main.py                 # Routes: /register, /users, /run-scheduler
│   ├── models.py               # SQLAlchemy models
│   ├── database.py             # Neon PostgreSQL connection
│   ├── email_sender.py         # Resend integration
│   └── alembic/                # Database migrations
│
├── frontend-admin/             # Admin panel
├── .github/workflows/          # CI/CD pipelines
└── requirements.txt
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/register` | Register a new user with email, categories, delivery time |
| `GET` | `/users` | Returns list of all registered users |
| `GET` | `/run-scheduler` | Triggered by cron — scrapes jobs, sends emails |

**Register Request Body**
```json
{
  "email": "you@example.com",
  "categories": ["Cybersecurity", "AI/ML", "Remote"],
  "delivery_time": "09:00 AM"
}
```

**Register Response**
```json
{
  "message": "User registered successfully",
  "email": "you@example.com"
}
```

---

## Local Development

### Prerequisites
- Node.js 18+
- Python 3.10+
- A Neon database URL
- A Resend API key

### Frontend
```bash
cd frontend
npm install
cp .env.example .env          # add VITE_API_BASE_URL
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head           # run migrations
uvicorn main:app --reload
```

### Environment Variables

**Frontend** (`.env`)
```env
VITE_API_BASE_URL=https://your-azure-backend.azurewebsites.net
```

**Backend** (`.env`)
```env
DATABASE_URL=postgresql://...   # Neon connection string
RESEND_API_KEY=re_...
```

---

## Deployment

### Frontend → Vercel
1. Connect repository to Vercel
2. Set root directory to `frontend`
3. Add `VITE_API_BASE_URL` environment variable
4. Deploy — Vercel auto-deploys on every push to `main`

### Backend → Azure App Service
1. Push to `main` — GitHub Actions handles build + deploy
2. Set application settings in Azure portal (env vars)
3. Alembic migrations run automatically on startup

### Scheduler → cron-job.org
- Hits `GET /run-scheduler` daily
- Each user receives their digest at their registered delivery time
- Lightweight scheduler architecture using external cron triggers

---

## Frontend Architecture Decisions

| Decision | Why |
|---|---|
| No UI framework (Tailwind/MUI) | Full control over design tokens, zero class bloat, ~0kb framework overhead |
| `useCallback` on all async handlers | Prevents stale closures and unnecessary re-renders |
| `Array.isArray()` guard on API response | Protects UI from malformed backend payloads |
| `if (loading) return` at top of submit | Prevents duplicate API calls on spam clicks |
| `mounted` flag in `useEffect` | Prevents React state updates on unmounted components (memory leak prevention) |
| `scroll-padding-top: 80px` | Fixed navbar doesn't overlap anchor targets |
| `type="button"` on all buttons | Prevents accidental form submissions |
| `will-change: transform` on animations | GPU-accelerated — smooth on low-end devices |
| `aria-live` on status banners | Screen readers announce success/error dynamically |
| `font-size: max(14px, 1em)` on inputs | Prevents iOS Safari auto-zoom on focus |

---

## Production Reliability Improvements

> The scheduler architecture separates onboarding email workflows from recurring scheduled delivery to prevent duplicate sends and ensure clean delivery state across user registration and alert cycles.

- Scheduler-safe recurring delivery logic
- Duplicate email prevention
- Onboarding and scheduler email separation
- Alembic-based schema migrations
- Persistent deployment pipelines
- Environment-based configuration management
- Database-backed delivery tracking
- Timezone-normalized scheduling

---

## License

[MIT](LICENSE) — built by [hgdttf](https://github.com/hgdttf)

---

<div align="center">

**If this helped you, consider starring the repo ⭐**

</div>
