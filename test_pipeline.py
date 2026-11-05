import sqlite3
from concurrent.futures import ThreadPoolExecutor
import fitz
from fastapi.testclient import TestClient
import app
import data
import report_data
import render

def test_pipeline(tmp_path, monkeypatch):
    db=tmp_path/'report.db'
    for module in [app,data,report_data,render]:
        monkeypatch.setattr(module,'DB',db)
    monkeypatch.setattr(app,'REPORTS',tmp_path/'reports')
    assert data.seed()==200
    assert data.seed()==200
    report=report_data.getReportData()
    assert report['total_orders']==200 and len(report['top_products'])==5
    assert len(report['orders_per_day'])<=7
    with ThreadPoolExecutor(2) as pool:
        replies=list(pool.map(lambda _:TestClient(app.app).post('/reports'),range(2)))
    assert sorted(r.status_code for r in replies)==[200,201]
    assert replies[0].json()['id']==replies[1].json()['id']
    assert len(list((tmp_path/'reports').glob('*.pdf')))==1
    client=TestClient(app.app)
    pdf=client.get(replies[0].json()['file'])
    assert pdf.headers['content-type']=='application/pdf'
    doc=fitz.open(stream=pdf.content,filetype='pdf')
    assert len(doc)>=2
    for page in list(doc)[1:]:
        assert all(h in page.get_text() for h in ['ID','Customer','Product','Amount','Date'])
    assert client.get('/reports/missing').status_code==404
    assert client.get('/reports/missing/file').status_code==404
    fresh=client.post('/reports',json={'force':True})
    assert fresh.status_code==201 and fresh.json()['id']!=replies[0].json()['id']
