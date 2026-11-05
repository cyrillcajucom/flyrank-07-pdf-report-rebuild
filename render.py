import datetime
import html
import sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright
from data import DB
from report_data import getReportData

ROOT = Path(__file__).parent
REPORTS = ROOT / 'reports'

def table(headers, rows):
    cells = lambda row, tag: ''.join(f'<{tag}>{html.escape(str(v))}</{tag}>' for v in row)
    return '<table><thead><tr>'+cells(headers,'th')+'</tr></thead><tbody>'+''.join('<tr>'+cells(row,'td')+'</tr>' for row in rows)+'</tbody></table>'

def build_html(data, rows):
    document = '''<!doctype html><html><head><meta charset="utf-8"><style>
    body { font: 12px Arial; color: #172333; } h1 { font-size: 25px; }
    table { border-collapse: collapse; width: 100%; margin: 14px 0 24px; }
    td, th { border-bottom: 1px solid #ccd4d9; padding: 8px; text-align: left; }
    th { background: #e6f0ef; } thead { display: table-header-group; }
    tr { break-inside: avoid; } h2 { break-after: avoid; }
    .details { break-before: page; }
    </style></head><body>'''
    document += f'<h1>Shop report — {datetime.date.today().isoformat()}</h1><p>Total orders: {data["total_orders"]} | Total revenue: {data["total_revenue"]:.2f}</p>'
    document += '<h2>Top five products by revenue</h2>'+table(['Product','Revenue'],[(r['product'],f"{r['revenue']:.2f}") for r in data['top_products']])
    document += '<h2>Orders per day — last seven days</h2>'+table(['Date','Orders'],[(r['day'],r['orders']) for r in data['orders_per_day']])
    document += '<h2 class="details">All orders</h2>'+table(['ID','Customer','Product','Amount','Date'],rows)
    return document+'</body></html>'

def render(path):
    data = getReportData()
    with sqlite3.connect(DB) as db:
        rows = db.execute('SELECT id,customer,product,amount,created_at FROM orders ORDER BY id').fetchall()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.set_content(build_html(data, rows))
            page.pdf(path=str(path), format='A4', print_background=True, margin={'top':'18mm','bottom':'18mm','left':'15mm','right':'15mm'})
        finally:
            browser.close()
    return path

if __name__ == '__main__':
    print(render(REPORTS/'test.pdf'))
