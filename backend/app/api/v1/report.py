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
        raise HTTPException(status_code=400, detail="No file uploaded.")
        
    try:
        file_bytes = await file.read()
        filename = file.filename or "uploaded_fir.txt"
        
        # Check for empty file upload
        if not file_bytes or len(file_bytes.strip()) == 0:
            raise HTTPException(
                status_code=400, 
                detail="The uploaded file is empty (0 bytes). Please upload a valid FIR PDF, image, or text file."
            )
        
        result = await report_service.generate_comprehensive_report(file_bytes, filename)
        
        if result.get("status") == "failed":
            raise HTTPException(
                status_code=422, 
                detail=result.get("error", "Failed to extract legal entities from FIR document.")
            )
            
        return result
        
    except HTTPException:
        # Re-raise explicit HTTP exceptions without transforming them to 500
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal pipeline error: {str(e)}")

