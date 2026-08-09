from fastapi import APIRouter, HTTPException

router = APIRouter()

# 🟢 TYPE YOURSELF: Practice creating API routes in FastAPI.
# Uncomment or type the code below.
#
# Why this file exists: It handles all lawyer research queries, searching
# local databases (Qdrant + Mongo) and fallback web sources.
#
# Common mistake: Forgetting to handle exceptions when DB is down.
#
# How it will evolve: Later we will add dense vector similarity search, 
# sparse BM25 query logic, and MongoDB document fetchers.

from app.services.ai_service import ai_service

@router.get("/search")
async def search_cases(q: str, limit: int = 5):
    """
    Endpoint to search for relevant criminal cases.
    Queries Qdrant vector database using dense embeddings.
    """
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
    results = await ai_service.search_legal_database(query=q, limit=limit)
    return {
        "query": q,
        "results": results
    }


@router.get("/document/{doc_id}")
async def get_document(doc_id: str):
    """
    Endpoint to retrieve the full document context from MongoDB.
    """
    if not doc_id:
        raise HTTPException(status_code=400, detail="Document ID is required")
        
    return await ai_service.get_document_by_id(doc_id)