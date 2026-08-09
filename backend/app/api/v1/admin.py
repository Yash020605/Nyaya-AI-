from fastapi import APIRouter, BackgroundTasks, HTTPException

router = APIRouter()

# Simple mock worker representing the future ingestion pipeline
def mock_ingestion_worker(doc_id: str, text: str):
    print(f"Background task starting: Ingesting document {doc_id}")
    # Simulating chunking, embedding generation, and Qdrant upserts
    print(f"Document {doc_id} successfully indexed in Qdrant.")

# 🟢 TYPE YOURSELF: Practice using FastAPI BackgroundTasks.
# Uncomment or type the code below.
#
# Why this file exists: To let administrators upload judgments and Acts
# which are asynchronously parsed, embedded, and index-synced in Qdrant.
#
# Common mistake: Running long CPU-bound tasks directly inside the request handler,
# which locks the event loop. Always use BackgroundTasks or a task queue.
#
# How it will evolve: Later we will connect this to a real Text Splitter,
# an embedding service, MongoDB models, and Qdrant clients.

@router.post("/ingest")
async def ingest_document(payload: dict, background_tasks: BackgroundTasks):
    """
    Endpoint to upload and ingest a new judgment.
    Immediately returns a status code 202 (Accepted) and processes in background.
    """
    title = payload.get("title")
    text = payload.get("text")
    citation = payload.get("citation")
    
    if not title or not text or not citation:
        raise HTTPException(status_code=400, detail="Title, text, and citation are required.")
        
    # Mock MongoDB insert
    mock_mongo_id = "mongo_id_98765"
#     
    # 🟢 Hand-type this background tasks enqueue
    background_tasks.add_task(mock_ingestion_worker, mock_mongo_id, text)
    return {
        "message": "Ingestion task initiated successfully.",
        "mongo_id": mock_mongo_id,
        "status": "processing"
    }
