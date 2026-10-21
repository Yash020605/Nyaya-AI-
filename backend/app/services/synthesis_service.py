import os
import json
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    logger.warning("GOOGLE_API_KEY environment variable not set. LLM synthesis will fail.")

class SynthesisService:
    def __init__(self):
        self.model_name = "gemini-1.5-pro" # Use the Pro model for deeper reasoning and reporting

    def generate_judicial_report(
        self,
        fir_data: dict,
        retrieved_statutes: list,
        retrieved_cases: list,
        matched_suspects: list = None,
        predicted_risk: str = "Unknown"
    ) -> str:
        """
        Generates a comprehensive judicial report by synthesizing the extracted FIR data,
        relevant statutory laws, historical case precedents, and ML-retrieved criminal profiles.
        """
        try:
            model = genai.GenerativeModel(model_name=self.model_name)
            
            # Formatting the retrieved context
            statutes_context = "\n".join([f"- {s['metadata'].get('act_name', '')} {s['metadata'].get('section_number', '')}: {s['metadata'].get('title', '')}" for s in retrieved_statutes])
            cases_context = "\n".join([f"- {c['metadata'].get('court_name', '')} ({c['metadata'].get('year', '')}) [Doc ID: {c['metadata'].get('original_case_id', '')}]: Match Score {c['score']:.2f}" for c in retrieved_cases])
            
            suspects_context = ""
            if matched_suspects:
                suspects_context = "\n".join([
                    f"- {s.get('name')} (Alias: {s.get('alias')}) | Similarity: {s.get('similarity_score')} | MO: {s.get('modus_operandi')} | Prior Convictions: {s.get('prior_convictions', 0)} | Risk: {s.get('risk_level', 'N/A')}"
                    for s in matched_suspects
                ])

            prompt = f"""You are an elite Indian legal strategist and judicial assistant. 
Based on the extracted First Information Report (FIR) details, the relevant statutory laws, semantic case precedents, and criminal record matches provided below, generate a 'Comprehensive Judicial Report'.

### 1. FIR Facts
- Summary: {fir_data.get('incident_summary', 'N/A')}
- Applied Laws (Police): {", ".join(fir_data.get('applied_laws', []))}
- Date: {fir_data.get('incident_date', 'N/A')}
- Location: {fir_data.get('incident_location', 'N/A')}
- Suspect Descriptions: {fir_data.get('suspect_details', 'N/A')}

### 2. Retrieved Statutory Law Context (IPC/BNS/BNSS)
{statutes_context if statutes_context else "No specific statutory text retrieved."}

### 3. Matched Prior Criminal Profiles (ML Pattern & MO Matching)
Predicted Incident Risk: {predicted_risk}
{suspects_context if suspects_context else "No prior suspect records matched."}

### 4. Retrieved Case Precedent Context
{cases_context if cases_context else "No historical case precedents retrieved."}

### Output Instructions
Write a formal, structured Comprehensive Judicial Report containing:
1. **Case Overview**: A professional summary of the allegations and incident facts.
2. **Statutory Analysis**: An analysis of whether the applied police charges match the statutory definitions retrieved. Highlight if any charges seem excessive, misapplied, or missing.
3. **Suspect & Criminal History Analysis**: Analyze the matched criminal profiles, their Modus Operandi (MO), and recidivism risk.
4. **Precedent Synthesis**: Discuss how the retrieved historical cases align with this FIR summary. 
5. **Strategic Recommendations**: Next steps for an advocate representing the defense or the prosecution based on evidence and legal precedents.

Do not hallucinate laws or cases not provided in the context above. Keep the tone strictly legal and objective.
"""
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"LLM Synthesis Error: {e}")
            return f"Error generating judicial report: {str(e)}"

synthesis_service = SynthesisService()
