from fastapi import FastAPI
app = FastAPI(title='Shop PDF reports')
@app.get('/health')
def health():
    return {'status': 'ok'}
