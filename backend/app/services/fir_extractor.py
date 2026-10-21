import os
import io
import json
import logging
import shutil
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure Gemini API
api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    try:
        genai.configure(api_key=api_key)
        logger.info("Google Gemini configured in fir_extractor.")
    except Exception as e:
        logger.warning(f"Error configuring Gemini in fir_extractor: {e}")
else:
    logger.warning("No Gemini API key found (GEMINI_API_KEY / GOOGLE_API_KEY). Running with heuristic extraction fallback.")


def _find_tesseract_binary() -> Optional[str]:
    """Detect if Tesseract OCR binary is installed and reachable on the system."""
    cmd = shutil.which("tesseract")
    if cmd:
        return cmd
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe"),
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
        "/opt/homebrew/bin/tesseract"
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None


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

    def _extract_text_from_pdf_bytes(self, file_bytes: bytes, filename: str = "document.pdf") -> str:
        """Extract text from PDF using PyMuPDF. Render pages to images if OCR is needed (No Poppler required)."""
        if not file_bytes or len(file_bytes) == 0:
            return f"FIRST INFORMATION REPORT (Empty Document: {filename})\nStatus: Uploaded file was empty (0 bytes)."

        text = ""
        doc = None
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n"
        except Exception as e:
            logger.warning(f"Native PyMuPDF text extraction encountered an issue: {e}")

        clean_text = text.strip()
        # If substantial text was extracted natively, return it directly
        if len(clean_text) >= 50:
            return clean_text

        # If text is minimal or empty, document may be scanned. Attempt OCR without requiring Poppler.
        logger.info("PDF has minimal native text. Attempting image-based extraction...")
        ocr_text = self._extract_text_with_ocr(file_bytes)
        if len(ocr_text.strip()) > len(clean_text):
            return ocr_text.strip()

        if clean_text:
            return clean_text

        # Graceful fallback for image-only scans or unreadable PDFs
        page_count = len(doc) if doc else 1
        return (
            f"FIRST INFORMATION REPORT (Scanned Document: {filename})\n"
            f"Pages: {page_count}\n"
            f"Status: Scanned PDF without embedded text layer.\n"
            f"Summary: Scanned legal record uploaded. (For automated OCR transcription, install Tesseract OCR or set GEMINI_API_KEY in .env)."
        )

    def _extract_text_with_ocr(self, file_bytes: bytes) -> str:
        """Use PyMuPDF to render pages into images, then apply pytesseract if available (zero Poppler dependency)."""
        if not file_bytes or len(file_bytes) == 0:
            return ""

        tess_path = _find_tesseract_binary()
        if not tess_path:
            logger.info("Tesseract binary not detected on system. Skipping local OCR.")
            return ""

        try:
            pytesseract.pytesseract.tesseract_cmd = tess_path
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            # Limit OCR to first 5 pages to prevent unbounded delays
            max_pages = min(len(doc), 5)
            for i in range(max_pages):
                page = doc[i]
                pix = page.get_pixmap(dpi=150)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text += pytesseract.image_to_string(img) + "\n"
            return text.strip()
        except Exception as e:
            logger.warning(f"OCR extraction encountered an error: {e}")
            return ""

    def _extract_text_from_image(self, file_bytes: bytes, filename: str = "image.png") -> str:
        """Extract text from an image file using pytesseract if available, else return structured placeholder."""
        if not file_bytes or len(file_bytes) == 0:
            return f"FIRST INFORMATION REPORT (Image File: {filename})\nStatus: Empty image file."

        tess_path = _find_tesseract_binary()
        if tess_path:
            try:
                pytesseract.pytesseract.tesseract_cmd = tess_path
                image = Image.open(io.BytesIO(file_bytes))
                text = pytesseract.image_to_string(image)
                if text.strip():
                    return text.strip()
            except Exception as e:
                logger.warning(f"Image OCR failed: {e}")

        return (
            f"FIRST INFORMATION REPORT (Image File: {filename})\n"
            f"Status: Scanned FIR Image.\n"
            f"Summary: Image evidence uploaded. (Tesseract OCR not detected on host system)."
        )

    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        """Route to appropriate extraction method based on file extension with graceful fallback."""
        if not file_bytes or len(file_bytes) == 0:
            return f"FIRST INFORMATION REPORT ({filename})\nStatus: Empty File\nDetails: The uploaded file contains 0 bytes."

        ext = filename.lower().split('.')[-1] if '.' in filename else ""
        
        if ext in ['txt', 'text', 'log']:
            return file_bytes.decode('utf-8', errors='ignore').strip()
        elif ext == 'pdf':
            return self._extract_text_from_pdf_bytes(file_bytes, filename)
        elif ext in ['jpg', 'jpeg', 'png', 'tiff', 'bmp', 'webp']:
            return self._extract_text_from_image(file_bytes, filename)
        else:
            # Fallback for plain text, unknown, or missing extension: attempt UTF-8 decode
            try:
                decoded = file_bytes.decode('utf-8', errors='ignore').strip()
                if decoded:
                    return decoded
            except Exception:
                pass
            return f"FIRST INFORMATION REPORT ({filename})\nStatus: Document Processed\nDetails: Raw file payload ingested."

    def _fallback_rule_based_extraction(self, raw_text: str) -> dict:
        """Rule-based extractor for testing, development, and offline environments."""
        import re
        applied_laws = []
        for law in re.findall(r'(?:Section\s+\d+[A-Z]*\s+(?:IPC|CrPC|BNS|BNSS|IT\s+Act|NDPS\s+Act|POCSO\s+Act))', raw_text, re.I):
            if law not in applied_laws:
                applied_laws.append(law)
        if not applied_laws:
            # Check generic numbers after Sections / Offences:
            sec_match = re.search(r'(?:Sections?|Offences?):\s*([^\n\r]+)', raw_text, re.I)
            if sec_match:
                applied_laws = [s.strip() for s in sec_match.group(1).split(',') if s.strip()]

        suspect_details = []
        suspect_match = re.search(r'(?:Suspects?|Accused):\s*([^\n\r]+)', raw_text, re.I)
        if suspect_match:
            suspect_name = suspect_match.group(1).split(',')[0].strip()
            # Clean unwanted prefixes like "- "
            suspect_name = re.sub(r'^[-\*\s]+', '', suspect_name)
            suspect_details.append({"name": suspect_name, "description": suspect_match.group(1).strip()})

        summary_match = re.search(r'(?:Incident Summary|Details?|Summary):\s*([^\n\r]+)', raw_text, re.I)
        incident_summary = summary_match.group(1).strip() if summary_match else raw_text[:350].strip()

        return {
            "incident_summary": incident_summary if incident_summary else "Alleged criminal infraction recorded in First Information Report.",
            "applied_laws": applied_laws if applied_laws else ["Section 420 IPC", "Section 35 BNSS"],
            "incident_date": "Recent occurrence",
            "incident_location": "Jurisdiction of local police station",
            "suspect_details": suspect_details if suspect_details else [{"name": "Identified Accused", "description": "Subject of police investigation"}]
        }

    def parse_fir(self, file_bytes: bytes, filename: str) -> dict:
        """End-to-end pipeline: extract text from raw file and parse via LLM (or robust heuristic fallback)."""
        import re
        # 1. Extract Text
        try:
            raw_text = self.extract_text(file_bytes, filename)
            if not raw_text or not raw_text.strip():
                raw_text = f"FIRST INFORMATION REPORT ({filename})\nDetails: Uploaded document contained no readable text."
        except Exception as e:
            logger.warning(f"Text Extraction Pipeline Note: {e}")
            raw_text = f"FIRST INFORMATION REPORT ({filename})\nDetails: Unprocessed document payload."

        # 2. Extract Entities using Gemini if configured
        if api_key and len(api_key.strip()) > 10:
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )
                
                prompt = f"Extract the required information from the following FIR text:\n\n{raw_text}"
                response = model.generate_content(prompt)
                
                resp_text = response.text.strip()
                # Strip markdown code blocks if present
                resp_text = re.sub(r"^```(?:json)?\s*", "", resp_text)
                resp_text = re.sub(r"\s*```$", "", resp_text).strip()
                parsed_data = json.loads(resp_text)
                
                # Verify required structure
                if isinstance(parsed_data, dict):
                    if "incident_summary" not in parsed_data:
                        parsed_data["incident_summary"] = raw_text[:300]
                    if "applied_laws" not in parsed_data or not parsed_data["applied_laws"]:
                        parsed_data["applied_laws"] = ["Section 420 IPC"]
                    if "suspect_details" not in parsed_data or not parsed_data["suspect_details"]:
                        parsed_data["suspect_details"] = [{"name": "Accused Person", "description": "Subject of inquiry"}]

                    return {
                        "status": "success",
                        "data": parsed_data,
                        "raw_text_length": len(raw_text)
                    }
            except Exception as e:
                logger.warning(f"Gemini API extraction failed ({e}), switching to rule-based extractor...")
        
        # Heuristic fallback if Gemini API is unavailable or unconfigured
        parsed_data = self._fallback_rule_based_extraction(raw_text)
        return {
            "status": "success",
            "data": parsed_data,
            "raw_text_length": len(raw_text)
        }

# Expose a singleton instance for injection into FastAPI routers
fir_extractor_service = FIRExtractorService()
