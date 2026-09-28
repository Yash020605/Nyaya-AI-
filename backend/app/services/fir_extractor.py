import os
import io
import json
import logging
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure Gemini API
# Assuming GOOGLE_API_KEY is loaded in the environment or core config
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    logger.warning("GOOGLE_API_KEY environment variable not set. LLM extraction will fail.")

class SuspectDetail(BaseModel):
    name: str = Field(..., description="Name of the suspect.")
    description: Optional[str] = Field(None, description="Physical description or any identifying details of the suspect.")

class FIRExtractionSchema(BaseModel):
    incident_summary: str = Field(..., description="A concise, factual summary of the crime and sequence of events.")
    applied_laws: List[str] = Field(..., description="A list of strings representing the specific penal codes applied by the police. Include both legacy codes (IPC/CrPC) and newly implemented BNS/BNSS sections if present.")
    incident_date: Optional[str] = Field(None, description="The date and time of the occurrence.")
    incident_location: Optional[str] = Field(None, description="The geographic location of the occurrence.")
    suspect_details: List[SuspectDetail] = Field(default_factory=list, description="List of suspects identified in the FIR along with their physical descriptions or details.")

class FIRExtractorService:
    def __init__(self):
        # We use gemini-1.5-flash for fast structured JSON outputs
        self.model_name = "gemini-1.5-flash"
        
        # System prompt for the LLM
        self.system_prompt = """You are an expert Indian legal data extractor. 
Your task is to analyze raw, often messy First Information Reports (FIRs) and extract critical entities.
Ignore all administrative boilerplate, police station metadata, and irrelevant signatures.
Focus entirely on extracting the core facts of the case into a structured format.

You MUST extract the following information:
1. `incident_summary`: A concise, factual summary of the crime, the sequence of events, and the allegations made by the complainant.
2. `applied_laws`: A list of strings representing the specific penal codes applied by the police. Actively identify and include both the legacy codes (e.g., IPC, CrPC, Evidence Act) and the newly implemented criminal laws (e.g., BNS, BNSS, BSA). Format them clearly (e.g., "Section 302 IPC", "Section 103 BNS").
3. `incident_date`: The date and time of the occurrence of the offense.
4. `incident_location`: The geographic location or address where the incident occurred.
5. `suspect_details`: A list of suspects identified in the FIR. For each suspect, extract their `name` and a `description` (physical attributes, clothing, identifying marks, or context of their involvement).

Output strictly in JSON format matching the requested schema. Do not include markdown formatting or backticks around the output.
"""

    def _extract_text_from_pdf_bytes(self, file_bytes: bytes) -> str:
        """Extract text from PDF using PyMuPDF. Fallback to OCR if it is a scanned document."""
        text = ""
        try:
            # Try native PDF text extraction
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()
                
            # If text is extremely short, it might be a scanned PDF image wrapper
            if len(text.strip()) < 50:
                logger.info("PDF appears to be scanned. Falling back to OCR extraction...")
                text = self._extract_text_with_ocr(file_bytes)
                
            return text.strip()
        except Exception as e:
            logger.error(f"Error in PDF text extraction: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    def _extract_text_with_ocr(self, file_bytes: bytes) -> str:
        """Use pdf2image and pytesseract to OCR a scanned PDF document."""
        try:
            images = convert_from_bytes(file_bytes)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise ValueError(f"Failed to perform OCR on document: {str(e)}. Make sure Tesseract and poppler are installed.")
            
    def _extract_text_from_image(self, file_bytes: bytes) -> str:
        """Extract text directly from an image file using pytesseract."""
        try:
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"Image text extraction failed: {e}")
            raise ValueError(f"Failed to extract text from image: {str(e)}")

    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        """Route to appropriate extraction method based on file extension."""
        ext = filename.lower().split('.')[-1]
        
        if ext == 'pdf':
            return self._extract_text_from_pdf_bytes(file_bytes)
        elif ext in ['jpg', 'jpeg', 'png', 'tiff', 'bmp']:
            return self._extract_text_from_image(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def parse_fir(self, file_bytes: bytes, filename: str) -> dict:
        """End-to-end pipeline: extract text from raw file and parse via LLM."""
        # 1. Extract Text
        try:
            raw_text = self.extract_text(file_bytes, filename)
            if not raw_text:
                raise ValueError("No text could be extracted from the document.")
        except Exception as e:
            logger.error(f"Text Extraction Pipeline Error: {e}")
            return {"error": str(e), "status": "failed"}

        # 2. Extract Entities using Gemini
        try:
            # Instantiate the model with structured output configuration
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.system_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            
            prompt = f"Extract the required information from the following FIR text:\n\n{raw_text}"
            
            response = model.generate_content(prompt)
            
            # Parse the JSON response
            result_json = response.text
            parsed_data = json.loads(result_json)
            
            return {
                "status": "success",
                "data": parsed_data,
                "raw_text_length": len(raw_text)
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"LLM returned invalid JSON: {e}. Raw response: {response.text}")
            return {"error": "LLM failed to return valid JSON format.", "status": "failed"}
        except Exception as e:
            logger.error(f"LLM Processing Error: {e}")
            return {"error": str(e), "status": "failed"}

# Expose a singleton instance for injection into FastAPI routers
fir_extractor_service = FIRExtractorService()
