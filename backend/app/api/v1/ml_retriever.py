from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.services.ml_retriever import custom_ml_retriever

router = APIRouter()

class SuspectProfileQuery(BaseModel):
    primary_crime_type: str = Field("Theft / Burglary", description="Crime type or MO classification")
    weapon_used: str = Field("None", description="Weapon identified (Firearm, Knife, Blunt Object, None, etc.)")
    gang_affiliation: str = Field("Independent", description="Known gang syndicate or Independent")
    state: str = Field("Maharashtra", description="State or operational jurisdiction")
    build: str = Field("Medium", description="Physical build (Slim, Medium, Athletic, Heavy)")
    complexion: str = Field("Wheatish", description="Physical complexion (Fair, Wheatish, Dark)")
    age: int = Field(28, ge=18, le=100, description="Approximate suspect age")
    height_cm: int = Field(172, ge=120, le=220, description="Suspect height in cm")
    prior_convictions: int = Field(1, ge=0, description="Number of prior recorded convictions")
    active_warrants: int = Field(0, ge=0, description="Number of active arrest warrants")
    top_k: int = Field(5, ge=1, le=20, description="Top matches to retrieve via KNN")

@router.post("/predict-and-match")
async def match_suspect_profiles(query: SuspectProfileQuery):
    """
    ML Profiling Endpoint:
    Uses trained Random Forest classifier to predict suspect recidivism/risk tier,
    and KNN Retriever (cosine metric) to fetch Top-K matching criminal records from 1,000 dataset.
    """
    if not custom_ml_retriever.is_loaded:
        raise HTTPException(
            status_code=503, 
            detail="ML models are not loaded in memory. Ensure weights are trained."
        )

    result = custom_ml_retriever.predict_and_match(
        primary_crime_type=query.primary_crime_type,
        weapon_used=query.weapon_used,
        gang_affiliation=query.gang_affiliation,
        state=query.state,
        build=query.build,
        complexion=query.complexion,
        age=query.age,
        height_cm=query.height_cm,
        prior_convictions=query.prior_convictions,
        active_warrants=query.active_warrants,
        top_k=query.top_k
    )

    if "error" in result and result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])

    return result
