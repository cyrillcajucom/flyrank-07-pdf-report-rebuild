import datetime
import random
import sqlite3
from pathlib import Path

DB = Path(__file__).parent / 'report.db'

def init_db():
    with sqlite3.connect(DB) as db:
        db.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT, product TEXT, amount REAL, created_at TEXT)')

def seed():
    init_db()
    rng = random.Random(42)
    today = datetime.date.today()
    with sqlite3.connect(DB) as db:
        db.execute('DELETE FROM orders')
        db.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', [
            (i+1, f'Customer {i%20+1}', rng.choice(['Notebook','Pen','Book','Bag','Mug','Lamp']),
             round(rng.uniform(5,200),2), (today-datetime.timedelta(days=rng.randrange(30))).isoformat())
            for i in range(200)
        ])
        return db.execute('SELECT COUNT(*) FROM orders').fetchone()[0]

if __name__ == '__main__':
    print(f'Seeded {seed()} orders')
