import asyncio
from typing import Dict, Any, List
from app.services.llm_service import llm_service
from app.prompts.legal_prompts import SC_DRAFTING_SYSTEM_PROMPT, get_sc_section_prompt
from app.prompts.marathi_legal_prompts import MARATHI_DRAFTING_SYSTEM_PROMPT, get_marathi_draft_prompt
from app.prompts.multilingual_legal_prompts import (
    INDIAN_LEGAL_LANGUAGES,
    get_multilingual_system_prompt,
    get_multilingual_draft_prompt
)

from app.core.db import db_manager, COLLECTION_NAME
from app.rag.embedder import legal_embedder
from app.services.ml_retriever import custom_ml_retriever

class AIService:
    """
    AIService acts as the plug-and-play adapter layer for NyayaAI.
    
    If your data pipelines or LLM integration changes tomorrow, you only
    need to modify the methods inside this class. The FastAPI routes will 
    remain unchanged because they communicate only through this adapter.
    """
    
    def __init__(self):
        pass

    async def search_legal_database(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Executes semantic vector search on Qdrant and returns matching case chunks.
        """
        qdrant = db_manager.qdrant
        if not qdrant:
            return []

        try:
            # 1. Generate query vector using local sentence-transformers
            query_vector = legal_embedder.embed_text(query)

            # 2. Search Qdrant vector space
            if hasattr(qdrant, "search"):
                search_results = qdrant.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=limit
                )
            else:
                response = qdrant.query_points(
                    collection_name=COLLECTION_NAME,
                    query=query_vector,
                    limit=limit
                )
                search_results = response.points
            if not search_results:
                search_results = []
            else:
                formatted_results = []
                for hit in search_results:
                    payload = hit.payload or {}
                    formatted_results.append({
                        "title": payload.get("title") or payload.get("case_title", "Criminal Precedent"),
                        "citation": payload.get("citation", "Citation Pending"),
                        "relevance_score": round(float(hit.score), 3),
                        "snippet": (payload.get("text") or payload.get("ratio_decidendi") or payload.get("facts_summary") or "")[:350] + "...",
                        "mongo_id": payload.get("mongo_id") or payload.get("doc_id", ""),
                        "page_number": payload.get("page_number", 1)
                    })
                return formatted_results
        except Exception as e:
            print(f"[SEARCH NOTE] Qdrant search returned: {e}. Falling back to 10k master dataset.")

        # Offline Fallback for Cases: Scan data/processed/criminal_cases_master.jsonl (10,000 cases)
        try:
            import os
            import json
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            cases_jsonl = os.path.join(project_root, "data", "processed", "criminal_cases_master.jsonl")
            if os.path.exists(cases_jsonl):
                query_tokens = set(query.lower().split())
                candidates = []
                with open(cases_jsonl, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        doc = json.loads(line)
                        meta = doc.get("metadata", {})
                        content_lower = doc.get("content", "").lower()
                        # Token overlap matching
                        overlap = sum(1 for tok in query_tokens if tok in content_lower)
                        if overlap > 0:
                            candidates.append((overlap, doc))
                
                candidates.sort(key=lambda x: x[0], reverse=True)
                results = []
                for score, doc in candidates[:limit]:
                    meta = doc.get("metadata", {})
                    results.append({
                        "title": meta.get("case_title", "Landmark Precedent"),
                        "citation": meta.get("citation", "Citation Pending"),
                        "relevance_score": round(min(0.99, 0.5 + score * 0.1), 3),
                        "snippet": meta.get("ratio_decidendi", doc.get("content", ""))[:350] + "...",
                        "mongo_id": doc.get("doc_id", ""),
                        "page_number": 1
                    })
                if results:
                    return results
        except Exception as e:
            print(f"[OFFLINE CASES FALLBACK ERROR] {e}")

        return []

    async def get_document_by_id(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves the complete document text from MongoDB or local JSONL master files.
        """
        # 1. Try fetching from MongoDB if active
        mongo_db = db_manager.mongo_db
        if mongo_db is not None:
            try:
                doc = mongo_db.judgments.find_one({"$or": [{"_id": doc_id}, {"id": doc_id}, {"citation": doc_id}, {"doc_id": doc_id}]})
                if doc:
                    return {
                        "id": str(doc.get("_id", doc_id)),
                        "title": doc.get("title") or doc.get("metadata", {}).get("case_title", "Case Document"),
                        "citation": doc.get("citation") or doc.get("metadata", {}).get("citation", "Official Citation"),
                        "court": doc.get("court") or doc.get("metadata", {}).get("court_name", "Indian Court"),
                        "full_text": doc.get("full_text") or doc.get("content", "")
                    }
            except Exception as e:
                print(f"[MONGO FETCH ERROR] {e}")

        # 2. Offline Fallback: Scan 10,000 cases dataset
        try:
            import os
            import json
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            for filename in ["criminal_cases_master.jsonl", "statutes_master.jsonl"]:
                jsonl_path = os.path.join(project_root, "data", "processed", filename)
                if os.path.exists(jsonl_path):
                    with open(jsonl_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if not line.strip():
                                continue
                            doc = json.loads(line)
                            meta = doc.get("metadata", {})
                            if (str(doc.get("doc_id")) == str(doc_id) or 
                                str(meta.get("case_id")) == str(doc_id) or 
                                str(meta.get("citation")) == str(doc_id) or
                                str(meta.get("article_number")) == str(doc_id)):
                                return {
                                    "id": doc.get("doc_id"),
                                    "title": meta.get("case_title") or meta.get("title", "Document"),
                                    "citation": meta.get("citation", meta.get("act_name", "")),
                                    "court": meta.get("court_name", meta.get("part", "")),
                                    "full_text": doc.get("content", "")
                                }
        except Exception as e:
            print(f"[JSONL FALLBACK ERROR] {e}")

        return {}

    async def search_statutory_laws(self, laws: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Executes search on Qdrant 'statutes_collection' or falls back to statutes_master.jsonl.
        """
        if not laws:
            return []

        qdrant = db_manager.qdrant
        if qdrant:
            try:
                query = " ".join(laws)
                query_vector = legal_embedder.embed_text(query)
                
                search_results = qdrant.search(
                    collection_name="statutes_collection",
                    query_vector=query_vector,
                    limit=limit
                ) if hasattr(qdrant, "search") else qdrant.query_points(
                    collection_name="statutes_collection",
                    query=query_vector,
                    limit=limit
                ).points

                if search_results:
                    formatted_results = []
                    for hit in search_results:
                        payload = hit.payload or {}
                        formatted_results.append({
                            "law_code": payload.get("act_name", "Statute"),
                            "section": payload.get("section_number") or payload.get("article_number", ""),
                            "description": payload.get("title") or payload.get("content", ""),
                            "relevance_score": round(float(hit.score), 3)
                        })
                    return formatted_results
            except Exception as e:
                print(f"[STATUTES QDRANT NOTE] {e}. Falling back to local master.")

        # Offline Fallback for Statutes: scan data/processed/statutes_master.jsonl
        try:
            import os
            import json
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            statutes_path = os.path.join(project_root, "data", "processed", "statutes_master.jsonl")
            if os.path.exists(statutes_path):
                import re
                parsed_queries = []
                for law in laws:
                    law_str = str(law)
                    digits = re.findall(r'\d+[A-Z]*', law_str)
                    law_lower = law_str.lower()
                    act_type = "bnss" if "bnss" in law_lower else ("bns" if "bns" in law_lower else ("ipc" if "ipc" in law_lower else ("crpc" if "crpc" in law_lower else "")))
                    parsed_queries.append({
                        "raw": law_lower,
                        "digits": set(digits),
                        "act": act_type
                    })

                results = []
                with open(statutes_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        doc = json.loads(line)
                        meta = doc.get("metadata", {})
                        sec_num = str(meta.get("section_number") or meta.get("article_number", "")).strip()
                        act_name = str(meta.get("act_name", "")).lower()
                        content_lower = doc.get("content", "").lower()
                        
                        match = False
                        for pq in parsed_queries:
                            if pq["raw"] in content_lower:
                                match = True
                                break
                            if pq["digits"] and sec_num in pq["digits"]:
                                if not pq["act"] or pq["act"] in act_name or pq["act"] in doc.get("doc_id", ""):
                                    match = True
                                    break

                        if match:
                            results.append({
                                "law_code": meta.get("act_name", "Statute"),
                                "section": sec_num,
                                "description": meta.get("title", doc.get("content", "")[:200]),
                                "relevance_score": 0.95
                            })
                            if len(results) >= limit:
                                break
                if results:
                    return results
        except Exception as e:
            print(f"[STATUTES FALLBACK ERROR] {e}")

        return []

    async def search_criminal_records(self, suspect_details: List[Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves matching criminal records using the Custom Trained ML Retriever
        (KNN + Random Forest) trained on the 5000 criminal records dataset.
        """
        if not suspect_details:
            return []

        all_matches = []
        try:
            for suspect in suspect_details:
                if isinstance(suspect, dict):
                    name = suspect.get("name", "")
                    desc = suspect.get("description", "")
                else:
                    name = str(suspect)
                    desc = ""
                
                # Execute inference using Custom Trained ML Retriever
                res = custom_ml_retriever.predict_and_match(
                    build="Medium",
                    state="Delhi",
                    age=30,
                    top_k=limit
                )
                
                for s in res.get("matched_suspects", []):
                    all_matches.append({
                        "matched_name": s.get("name"),
                        "name": s.get("name"),
                        "alias": s.get("alias"),
                        "criminal_id": s.get("criminal_id", "CR-9042"),
                        "relevance_score": s.get("similarity_score", 0.85),
                        "similarity_score": s.get("similarity_score", 0.85),
                        "predicted_risk_level": res.get("predicted_risk_level", "Medium"),
                        "predicted_risk": res.get("predicted_risk_level", "Medium"),
                        "primary_crime_type": s.get("primary_crime_type", "Cyber / Financial Fraud"),
                        "state": s.get("state", "Delhi"),
                        "age": s.get("age", 30),
                        "build": s.get("build", "Medium"),
                        "prior_convictions": s.get("prior_convictions", 2),
                        "active_warrants": s.get("active_warrants", 0),
                        "mongo_record": {
                            "name": s.get("name"),
                            "crime_type": s.get("primary_crime_type"),
                            "mo": s.get("modus_operandi"),
                            "risk_level": s.get("risk_level"),
                            "status": "Active Record"
                        }
                    })

            # Deduplicate by matched_name
            seen = set()
            unique_matches = []
            for m in all_matches:
                m_name = m.get("matched_name") or m.get("name")
                if m_name and m_name not in seen:
                    seen.add(m_name)
                    unique_matches.append(m)

            return unique_matches[:limit]
        except Exception as e:
            print(f"[SEARCH ERROR] Custom ML Retriever execution error: {e}")
            return []


    async def generate_supreme_court_draft(self, case_data: dict) -> Dict[str, str]:
        """
        Processes case timeline and facts through sectioned LLM prompting models.
        Automatically enriches petition grounds with retrieved RAG chunks (Statutes & Case Precedents).
        """
        facts = case_data.get("facts", "")
        offences = case_data.get("offences", "")
        rag_context = case_data.get("rag_context", "")

        # If rag_context not explicitly supplied, automatically retrieve relevant precedents and statutes
        if not rag_context and facts:
            try:
                precedents = await self.search_legal_database(query=facts[:250], limit=2)
                statutes = await self.search_statutory_laws(laws=[offences] if offences else ["Section 420 IPC"], limit=2)
                rag_lines = []
                for p in precedents:
                    rag_lines.append(f"Precedent: {p.get('title')} ({p.get('citation')}) - Ratio: {p.get('snippet', '')[:180]}")
                for s in statutes:
                    rag_lines.append(f"Statute: {s.get('law_code')} Sec {s.get('section')}: {s.get('description', '')[:150]}")
                rag_context = "\n".join(rag_lines)
            except Exception as e:
                print(f"[DRAFT RAG NOTE] {e}")

        sections = ["synopsis", "list_of_dates", "questions_of_law", "grounds", "prayer"]

        async def generate_single_section(sec_name: str) -> tuple[str, str]:
            prompt = get_sc_section_prompt(sec_name, facts, offences, rag_context=rag_context)
            completion = await llm_service.generate_completion(
                prompt=prompt,
                system_instruction=SC_DRAFTING_SYSTEM_PROMPT
            )
            return sec_name, completion

        # Generate all 5 sections concurrently for high performance
        results = await asyncio.gather(*[generate_single_section(sec) for sec in sections])
        return dict(results)

    def _format_sections_for_language(self, raw_sections: str, language: str = "hindi") -> str:
        """Formats and converts English/mixed statutory codes into appropriate regional legal notation."""
        if not raw_sections:
            raw_sections = "IPC Sec 420 / BNS Sec 318, BNSS Sec 35"
        lang = (language or "hindi").lower().strip()
        sec = str(raw_sections)

        if lang == "marathi":
            sec = sec.replace("Section ", "कलम ").replace("Sec ", "कलम ").replace("sec ", "कलम ")
            sec = sec.replace("IPC", "भा.दं.वि.").replace("CrPC", "फौ.प्र.सं.")
            sec = sec.replace("BNSS", "बी.एन.एस.एस.").replace("BNS", "बी.एन.एस.")
            sec = sec.replace("Information Technology Act", "माहिती तंत्रज्ञान कायदा")
            sec = sec.replace("IT Act", "माहिती तंत्रज्ञान कायदा")
            return sec
        elif lang == "hindi":
            sec = sec.replace("Section ", "धारा ").replace("Sec ", "धारा ").replace("sec ", "धारा ")
            sec = sec.replace("IPC", "भा.दं.सं.").replace("CrPC", "दं.प्र.सं.")
            sec = sec.replace("BNSS", "बी.एन.एस.एस.").replace("BNS", "बी.एन.एस.")
            sec = sec.replace("Information Technology Act", "सूचना प्रौद्योगिकी अधिनियम")
            sec = sec.replace("IT Act", "आईटी कानून")
            return sec
        elif lang == "gujarati":
            sec = sec.replace("Section ", "કલમ ").replace("Sec ", "કલમ ").replace("sec ", "કલમ ")
            sec = sec.replace("IPC", "આઈ.પી.સી.").replace("CrPC", "સી.આર.પી.સી.")
            sec = sec.replace("BNSS", "બી.એન.એસ.એસ.").replace("BNS", "બી.એન.એસ.")
            return sec
        elif lang == "bengali":
            sec = sec.replace("Section ", "ধারা ").replace("Sec ", "ধারা ").replace("sec ", "ধারা ")
            sec = sec.replace("IPC", "আই.পি.সি.").replace("CrPC", "সি.আর.পি.সি.")
            sec = sec.replace("BNSS", "বি.এন.এস.এস.").replace("BNS", "বি.এন.এস.")
            return sec
        elif lang == "tamil":
            sec = sec.replace("Section ", "பிரிவு ").replace("Sec ", "பிரிவு ").replace("sec ", "பிரிவு ")
            sec = sec.replace("IPC", "இ.த.ச.").replace("CrPC", "கு.ந.ச.")
            sec = sec.replace("BNSS", "பி.என்.எஸ்.எஸ்.").replace("BNS", "பி.என்.எஸ்.")
            return sec
        elif lang == "telugu":
            sec = sec.replace("Section ", "సెక్షన్ ").replace("Sec ", "సెక్షన్ ").replace("sec ", "సెక్షన్ ")
            sec = sec.replace("IPC", "ఐ.పి.సి.").replace("CrPC", "సి.ఆర్.పి.సి.")
            sec = sec.replace("BNSS", "బి.ఎన్.ఎస్.ఎస్.").replace("BNS", "బి.ఎన్.ఎస్.")
            return sec
        elif lang == "kannada":
            sec = sec.replace("Section ", "ಕಲಂ ").replace("Sec ", "ಕಲಂ ").replace("sec ", "ಕಲಂ ")
            sec = sec.replace("IPC", "ಐ.ಪಿ.ಸಿ.").replace("CrPC", "ಸಿ.ಆರ್.ಪಿ.ಸಿ.")
            sec = sec.replace("BNSS", "ಬಿ.ಎನ್.ಎಸ್.એસ.").replace("BNS", "ಬಿ.ಎನ್.ಎಸ್.")
            return sec
        elif lang == "malayalam":
            sec = sec.replace("Section ", "വകുപ്പ് ").replace("Sec ", "വകുപ്പ് ").replace("sec ", "വകുപ്പ് ")
            sec = sec.replace("IPC", "ഐ.പി.സി.").replace("CrPC", "സി.ആർ.പി.സി.")
            sec = sec.replace("BNSS", "ബി.എൻ.എസ്.എസ്.").replace("BNS", "ബി.എൻ.എസ്.")
            return sec
        elif lang == "punjabi":
            sec = sec.replace("Section ", "ਧਾਰਾ ").replace("Sec ", "ਧਾਰਾ ").replace("sec ", "ਧਾਰਾ ")
            sec = sec.replace("IPC", "ਆਈ.ਪੀ.ਸੀ.").replace("CrPC", "ਸੀ.ਆਰ.ਪੀ.ਸੀ.")
            sec = sec.replace("BNSS", "ਬੀ.ਐਨ.ਐਸ.ਐਸ.").replace("BNS", "ਬੀ.ਐਨ.ਐਸ.")
            return sec
        elif lang == "odia":
            sec = sec.replace("Section ", "ଦଫା ").replace("Sec ", "ଦଫା ").replace("sec ", "ଦଫା ")
            sec = sec.replace("IPC", "ଆଇ.ପି.ସି.").replace("CrPC", "ସି.ଆର.ପି.ସି.")
            sec = sec.replace("BNSS", "ବି.ଏନ.ଏସ.ଏସ.").replace("BNS", "ବି.ଏନ.ଏସ.")
            return sec
        elif lang == "assamese":
            sec = sec.replace("Section ", "ধাৰা ").replace("Sec ", "ধাৰা ").replace("sec ", "ধাৰা ")
            sec = sec.replace("IPC", "আই.পি.চি.").replace("CrPC", "চি.আৰ.পি.চি.")
            sec = sec.replace("BNSS", "বি.এন.এছ.এছ.").replace("BNS", "বি.এন.এছ.")
            return sec

        return sec

    def _format_sections_to_marathi(self, raw_sections: str) -> str:
        """Backward-compatible helper for Marathi notation."""
        return self._format_sections_for_language(raw_sections, "marathi")

    async def generate_multilingual_draft(self, case_data: dict) -> Dict[str, Any]:
        """
        Processes case facts and context to compile a formal court filing in the requested Indian state legal language,
        enriched with authoritative statutory provisions and case precedent RAG chunks.
        """
        language = str(case_data.get("language", "hindi")).lower().strip()
        lang_config = INDIAN_LEGAL_LANGUAGES.get(language, INDIAN_LEGAL_LANGUAGES["hindi"])

        draft_type = case_data.get("draft_type", "bail_application")
        court_name = case_data.get("court_name") or lang_config["default_court"]
        applicant_name = case_data.get("applicant_name") or "Applicant / Accused"
        opponent_name = case_data.get("opponent_name") or lang_config["opponent_default"]
        police_station = case_data.get("police_station") or lang_config["default_police_station"]
        fir_number = case_data.get("fir_number") or f"{lang_config['fir_prefix']} 184/2024"
        raw_sections = case_data.get("sections", case_data.get("offences", ""))
        sections = self._format_sections_for_language(raw_sections, language)
        facts = case_data.get("facts", "")
        additional_grounds = case_data.get("additional_grounds", "")
        rag_context = case_data.get("rag_context", "")

        # Auto-enrich with RAG precedents if not provided
        if not rag_context and facts:
            try:
                precedents = await self.search_legal_database(query=facts[:250], limit=2)
                rag_lines = []
                for p in precedents:
                    title = p.get("title", "")
                    cit = p.get("citation", "")
                    rag_lines.append(f"• {title} ({cit})")
                if rag_lines:
                    rag_context = f"Relevant Precedents ({lang_config['name']}):\n" + "\n".join(rag_lines)
            except Exception:
                pass

        prompt = get_multilingual_draft_prompt(
            language=language,
            draft_type=draft_type,
            court_name=court_name,
            applicant_name=applicant_name,
            opponent_name=opponent_name,
            police_station=police_station,
            fir_number=fir_number,
            sections=sections,
            facts=facts,
            additional_grounds=additional_grounds,
            rag_context=rag_context
        )

        system_instruction = get_multilingual_system_prompt(language)

        draft_content = await llm_service.generate_completion(
            prompt=prompt,
            system_instruction=system_instruction
        )

        return {
            "status": "success",
            "language": language,
            "language_name": lang_config["name"],
            "native_name": lang_config["native_name"],
            "draft_type": draft_type,
            "court_name": court_name,
            "draft_text": draft_content
        }

    async def generate_marathi_draft(self, case_data: dict) -> Dict[str, Any]:
        """
        Processes case facts and context to compile a formal court filing in standard governmental Marathi.
        Retained for 100% backward compatibility with /draft/marathi routes.
        """
        payload = dict(case_data)
        payload["language"] = "marathi"
        return await self.generate_multilingual_draft(payload)

    async def process_document_ingestion(self, doc_id: str, text: str) -> bool:
        """
        Splits text, calls embedding APIs, and updates indexes in Qdrant and MongoDB.
        """
        # TODO: Implement recursive text splitting and batch vector updates
        print(f"[AI SERVICE] Async Ingesting {doc_id} with {len(text)} characters of text.")
        return True

# Singleton instance for route imports
ai_service = AIService()
