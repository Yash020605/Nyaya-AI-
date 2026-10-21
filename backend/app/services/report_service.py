import asyncio
import json
import logging
from typing import Dict, Any

from app.services.fir_extractor import fir_extractor_service
from app.services.ai_service import ai_service
from app.services.llm_service import llm_service
from app.services.citation_verifier import citation_verifier
from app.prompts.legal_prompts import COMPREHENSIVE_REPORT_PROMPT

from app.services.pipeline_orchestrator import pipeline_orchestrator

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self):
        pass

    async def generate_comprehensive_report(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Orchestrates the full pipeline using LangGraph StateGraph:
        Node 1: extract_fir
        Node 2: parallel_retrieve (Statutes, 10,000 Cases, ML Suspect Profiler)
        Node 3: synthesize_report
        Node 4: citation_audit
        """
        return await pipeline_orchestrator.run(file_bytes=file_bytes, filename=filename)
        # 1. Extract Entities
        logger.info(f"Extracting entities from {filename}...")
        extraction_result = fir_extractor_service.parse_fir(file_bytes, filename)
        
        if extraction_result.get("status") == "failed":
            return {"error": extraction_result.get("error"), "status": "failed"}
            
        extracted_data = extraction_result.get("data", {})
        incident_summary = extracted_data.get("incident_summary", "")
        applied_laws = extracted_data.get("applied_laws", [])
        suspect_details = extracted_data.get("suspect_details", [])
        
        logger.info("Entities extracted successfully. Starting ML retrievals...")

        # 2. Concurrently fetch Laws, Precedents, and Criminal Records
        async def fetch_laws():
            return await ai_service.search_statutory_laws(laws=applied_laws, limit=3)
            
        async def fetch_precedents():
            return await ai_service.search_legal_database(query=incident_summary, limit=3)
            
        async def fetch_criminal_records():
            return await ai_service.search_criminal_records(suspect_details=suspect_details, limit=3)

        laws_res, precedents_res, records_res = await asyncio.gather(
            fetch_laws(),
            fetch_precedents(),
            fetch_criminal_records()
        )
        
        logger.info("Retrievals complete. Synthesizing report...")

        # Format context for prompt
        laws_context = json.dumps(laws_res, indent=2) if laws_res else "No specific statutory texts retrieved."
        precedents_context = json.dumps(precedents_res, indent=2) if precedents_res else "No exact matching precedents found."
        records_context = json.dumps(records_res, indent=2) if records_res else "No prior criminal records found for the suspects."

        # 3. Generate Final Report using LLM
        prompt = COMPREHENSIVE_REPORT_PROMPT.format(
            incident_facts=json.dumps(extracted_data, indent=2),
            statutory_laws=laws_context,
            case_precedents=precedents_context,
            criminal_records=records_context
        )

        try:
            # We use LLMService which gracefully falls back (Gemini -> Groq -> Mock)
            report_text = await llm_service.generate_completion(prompt=prompt)
        except Exception as e:
            logger.error(f"Failed to generate report text: {e}")
            report_text = f"Error generating report: {str(e)}"

        # 4. Citation & Grounding Verification Loop (Audit for hallucinations)
        verification_audit = citation_verifier.verify_report_citations(
            generated_text=report_text,
            retrieved_statutes=laws_res,
            retrieved_cases=precedents_res
        )

        return {
            "status": "success",
            "extracted_entities": extracted_data,
            "retrievals": {
                "statutory_laws": laws_res,
                "case_precedents": precedents_res,
                "criminal_records": records_res
            },
            "citation_verification": verification_audit,
            "comprehensive_report": report_text
        }

# Global singleton
report_service = ReportService()
