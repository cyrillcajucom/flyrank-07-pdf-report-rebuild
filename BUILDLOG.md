# Build log

2026-11-05: reconstruction, not a recreation of historical work. Public repository created before implementation. Source of truth: all 13 pages of `W7 - PDF report generator (1).pdf`; required stages only.

## Stage 0
`python -m playwright install chromium`: exit 0. FastAPI TestClient GET /health: 200, {"status":"ok"}. requirements records Python dependencies. No rendering implementation yet.

## Stage 1
`python data.py` run twice: both print `Seeded 200 orders`; SELECT COUNT(*) stays 200. Built SQLite orders schema and deterministic six-product recipe (amounts 5–200; last 30 days). report.db is ignored.

## Stage 2
`python report_data.py`: valid JSON with four sections: total_orders=200, total_revenue=20019.01, five ranked products, seven daily buckets (2026-10-30 through 2026-11-05). Independently asserted top product revenues do not exceed total. Daily WHERE spans today and previous six dates, as required.
