from fastapi import APIRouter, HTTPException

router = APIRouter()

# 🟢 TYPE YOURSELF: Practice creating API routes in FastAPI.
# Uncomment or type the code below.
#
# Why this file exists: To provide lawyers with Supreme Court-standard
# petitions using a modular section-by-section drafting pipeline.
#
# Common mistake: Forgetting to validate input schemas (e.g. empty case facts).
#
# How it will evolve: Later we will connect this to Pydantic schemas and 
# an LLM service that consumes case timelines to draft distinct sections.

from app.services.ai_service import ai_service

@router.post("/draft")
async def generate_draft(case_data: dict):
    """
    Endpoint to initiate document drafting.
    Receives case details and compiles Supreme Court petition sections via LLM.
    """
    if "facts" not in case_data or not str(case_data.get("facts", "")).strip():
        raise HTTPException(status_code=400, detail="Case facts are required for drafting")
        
    drafts = await ai_service.generate_supreme_court_draft(case_data)
    
    return {
        "status": "success",
        "drafts": drafts
    }
