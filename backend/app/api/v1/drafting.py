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

@router.post("/draft/marathi")
async def generate_marathi_court_draft(case_data: dict):
    """
    Endpoint to generate court-ready criminal petitions and applications
    in formal governmental Marathi for Maharashtra District and Magistrate Courts.
    """
    if "facts" not in case_data or not str(case_data.get("facts", "")).strip():
        raise HTTPException(status_code=400, detail="केसची वस्तुस्थिती (Case facts) आवश्यक आहे.")
        
    result = await ai_service.generate_marathi_draft(case_data)
    return result

@router.post("/draft/regional")
async def generate_regional_court_draft(case_data: dict):
    """
    Endpoint to generate court-ready criminal petitions and applications
    in 11 official Indian state legal languages (Hindi, Marathi, Gujarati,
    Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Odia, Assamese).
    """
    if "facts" not in case_data or not str(case_data.get("facts", "")).strip():
        raise HTTPException(status_code=400, detail="Case facts (वस्तुस्थिती / तथ्य) are required for drafting.")
        
    result = await ai_service.generate_multilingual_draft(case_data)
    return result

@router.get("/languages")
async def get_supported_languages():
    """
    Returns the 11 supported Indian state legal languages with default court configurations.
    """
    from app.prompts.multilingual_legal_prompts import INDIAN_LEGAL_LANGUAGES
    return {
        "status": "success",
        "languages": [
            {
                "code": code,
                "name": info["name"],
                "native_name": info["native_name"],
                "states": info["states"],
                "default_court": info["default_court"],
                "default_police_station": info["default_police_station"],
                "fir_prefix": info["fir_prefix"]
            }
            for code, info in INDIAN_LEGAL_LANGUAGES.items()
        ]
    }
