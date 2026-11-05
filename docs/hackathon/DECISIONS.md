# Engineering Decisions & Trade-off Log · Project Sentinel - Self-Operating Charging Network

| Decision | Chosen Path | Rejected Alternative | Why |
|---|---|---|---|
| Frontend UI | Streamlit / Rapid React | Custom Webpack/Tailwind setup | Saves 6 hours of boilerplate styling |
| Data Layer | In-memory + Local JSON Fixture | PostgreSQL + Prisma migrations | Zero DB connection latency/auth issues during demo |
| Error Handling | Graceful mock fallback toast | Complex retry/backoff queue | Judges don't wait 30 seconds for retries |

### Next 3 Actions
1. Verify mock fallback fires within 1 second if backend returns 500.
2. Keep commit history clean and tagged (`v0.1-walking-skeleton`, `v1.0-demo-ready`).
