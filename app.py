import datetime
import sqlite3
import uuid
import threading
from pydantic import BaseModel

report_lock = threading.Lock()
class ReportRequest(BaseModel):
    force: bool = False
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from data import DB, init_db
from render import REPORTS, render

app = FastAPI(title='Shop PDF reports')

def init_reports():
    init_db()
    with sqlite3.connect(DB) as db:
        db.execute('CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, path TEXT, created_at TEXT)')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/reports')
def make_report(body: ReportRequest | None = None):
    init_reports()
    with report_lock, sqlite3.connect(DB) as db:
        today = datetime.date.today().isoformat()
        existing = db.execute('SELECT id,path FROM reports WHERE substr(created_at,1,10)=? ORDER BY created_at DESC LIMIT 1', (today,)).fetchone()
        if existing and not (body and body.force) and __import__('pathlib').Path(existing[1]).is_file():
            return JSONResponse({'id':existing[0], 'file':f'/reports/{existing[0]}/file'}, status_code=200)
        if db.execute('SELECT COUNT(*) FROM orders').fetchone()[0] == 0:
            raise HTTPException(400, 'Run python data.py first')
        report_id = str(uuid.uuid4())
        path = render(REPORTS / f'{report_id}.pdf')
        db.execute('INSERT INTO reports VALUES (?,?,?)', (report_id,str(path),datetime.datetime.now().isoformat()))
    return JSONResponse({'id': report_id,'file': f'/reports/{report_id}/file'}, status_code=201)

@app.get('/reports/{report_id}')
def get_report(report_id: str):
    init_reports()
    with sqlite3.connect(DB) as db:
        row = db.execute('SELECT id,path,created_at FROM reports WHERE id=?',(report_id,)).fetchone()
    if not row:
        raise HTTPException(404,'Report not found')
    return {'id':row[0], 'path':row[1], 'created_at':row[2], 'file':f'/reports/{row[0]}/file'}

@app.get('/reports/{report_id}/file')
def get_file(report_id: str):
    row = get_report(report_id)
    if not __import__('pathlib').Path(row['path']).is_file():
        raise HTTPException(404,'Report file not found')
    return FileResponse(row['path'],media_type='application/pdf',filename='shop-report.pdf')
