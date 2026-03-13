from fastapi import FastAPI, HTTPException
from app.db import check_db_connection, init_db, get_document, get_documents, insert_document
from app.schemas import DocumentCreate

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

@app.get("/documents/{id}")
def get_document_by_id(id: int):
    document = get_document(id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {"status": "ok", "result": document}

@app.post("/documents")
def create_document(document: DocumentCreate):
    id = insert_document(document)
    return {"status": "created", "id": id}

