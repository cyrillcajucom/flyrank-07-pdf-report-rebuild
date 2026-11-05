# Build log

2026-11-05: reconstruction, not a recreation of historical work. Public repository created before implementation. Source of truth: all 13 pages of `W7 - PDF report generator (1).pdf`; required stages only.

## Stage 0
`python -m playwright install chromium`: exit 0. FastAPI TestClient GET /health: 200, {"status":"ok"}. requirements records Python dependencies. No rendering implementation yet.

## Stage 1
`python data.py` run twice: both print `Seeded 200 orders`; SELECT COUNT(*) stays 200. Built SQLite orders schema and deterministic six-product recipe (amounts 5–200; last 30 days). report.db is ignored.
