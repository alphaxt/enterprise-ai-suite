"""
FastAPI Entry Point for DocuMind Enterprise RAG Hub
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"
SAMPLES_DIR = BASE_DIR.parent / "data" / "samples"
sys.path.append(str(BASE_DIR))

from rag_engine import HybridRAGEngine
from agent import DocumentIntelligenceAgent

app = FastAPI(
    title="DocuMind AI: Enterprise RAG Platform",
    description="Production-grade Document Intelligence Agent with Hybrid Retrieval, Citations & Guardrails",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
rag_engine = HybridRAGEngine()
agent = DocumentIntelligenceAgent(rag_engine)


def auto_load_samples():
    """Pre-loads sample documents so the portfolio demo is instantly functional."""
    if SAMPLES_DIR.exists():
        for file_path in SAMPLES_DIR.glob("*.txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                count = rag_engine.ingest_text(doc_name=file_path.name, content=content)
                print(f"[OK] Ingested sample {file_path.name} ({count} chunks)")
            except Exception as e:
                print(f"[WARN] Error loading sample {file_path.name}: {e}")


# Run initial ingestion
auto_load_samples()


# Pydantic Schemas
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
    doc_filter: Optional[str] = None


class IngestTextRequest(BaseModel):
    doc_name: str
    content: str


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "DocuMind-RAG-Engine"}


@app.get("/api/stats")
def get_stats():
    return rag_engine.get_stats()


@app.get("/api/documents")
def list_documents():
    stats = rag_engine.get_stats()
    return {"documents": stats["document_names"]}


@app.post("/api/query")
def process_query(payload: QueryRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    result = agent.answer_query(
        query=payload.query,
        top_k=payload.top_k or 3,
        doc_filter=payload.doc_filter
    )
    return result


@app.post("/api/upload")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None),
    doc_name: Optional[str] = Form(None)
):
    """Allows uploading raw text or text/markdown/pdf files to the vector index."""
    if file:
        filename = file.filename
        content_bytes = await file.read()
        try:
            content = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content = content_bytes.decode("latin-1")
    elif raw_text and doc_name:
        filename = doc_name
        content = raw_text
    else:
        raise HTTPException(status_code=400, detail="Provide either a file or raw_text with doc_name.")

    chunks_added = rag_engine.ingest_text(doc_name=filename, content=content)
    return {
        "message": f"Successfully indexed '{filename}'",
        "chunks_indexed": chunks_added,
        "total_stats": rag_engine.get_stats()
    }


# Serve static web interface
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "DocuMind RAG API is running. Visit /docs for Swagger specifications."}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"[INFO] Starting DocuMind AI Server at http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
