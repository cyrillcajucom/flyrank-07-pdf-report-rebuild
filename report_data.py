import datetime
import json
import sqlite3
from data import DB

SQL = {
    'totals': 'SELECT COUNT(*) AS total_orders, COALESCE(ROUND(SUM(amount),2),0) AS total_revenue FROM orders',
    'top_products': 'SELECT product, ROUND(SUM(amount),2) AS revenue FROM orders GROUP BY product ORDER BY revenue DESC, product LIMIT 5',
    'orders_per_day': "SELECT created_at AS day, COUNT(*) AS orders FROM orders WHERE created_at >= ? AND created_at <= ? GROUP BY created_at ORDER BY created_at",
}

def getReportData():
    today = datetime.date.today()
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        totals = dict(db.execute(SQL['totals']).fetchone())
        return {**totals,
                'top_products': [dict(r) for r in db.execute(SQL['top_products'])],
                'orders_per_day': [dict(r) for r in db.execute(SQL['orders_per_day'], ((today-datetime.timedelta(days=6)).isoformat(), today.isoformat()))]}

if __name__ == '__main__':
    print(json.dumps(getReportData(), indent=2))
