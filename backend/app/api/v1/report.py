from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.report_service import report_service

router = APIRouter()

@router.post("/generate")
async def generate_comprehensive_report(file: UploadFile = File(...)):
    """
    Endpoint to ingest a raw FIR document (PDF or Image) and generate 
    a Comprehensive Judicial Report including extracted laws, case precedents, 
    and suspect criminal records.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    try:
        file_bytes = await file.read()
        filename = file.filename
        
        result = await report_service.generate_comprehensive_report(file_bytes, filename)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error during extraction"))
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
