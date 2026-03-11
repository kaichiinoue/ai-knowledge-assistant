from fastapi import FastAPI
from app.db import check_db_connection, init_db, get_documents

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/db-health")
def db_health_check():
    result = check_db_connection()
    return {"status": "ok", "result": result}

@app.get("/documents")
def get_all_documents():
    result = get_documents()
    return {"status": "ok", "result": result}
