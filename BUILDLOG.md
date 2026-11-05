# Build log

2026-11-05: reconstruction, not a recreation of historical work. Public repository created before implementation. Source of truth: all 13 pages of `W7 - PDF report generator (1).pdf`; required stages only.

## Stage 0
`python -m playwright install chromium`: exit 0. FastAPI TestClient GET /health: 200, {"status":"ok"}. requirements records Python dependencies. No rendering implementation yet.

## Stage 1
`python data.py` run twice: both print `Seeded 200 orders`; SELECT COUNT(*) stays 200. Built SQLite orders schema and deterministic six-product recipe (amounts 5–200; last 30 days). report.db is ignored.

## Stage 2
`python report_data.py`: valid JSON with four sections: total_orders=200, total_revenue=20019.01, five ranked products, seven daily buckets (2026-10-30 through 2026-11-05). Independently asserted top product revenues do not exceed total. Daily WHERE spans today and previous six dates, as required.

## Stage 3
`python render.py`: exit 0; reports/test.pdf is a real eight-page Chromium A4 PDF. PyMuPDF checked page count and detail column headers on all seven detail pages. Generated fresh report-page-1.png and all-pages-review.png; visually reviewed contact sheet: all 200 rows intact, headers repeat, no clipped text. Print CSS uses break-inside:avoid and thead. Title includes today's date, totals, top five, last-seven-day breakdown and full detail.
