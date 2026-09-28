import asyncio
from typing import Dict, Any, List
from app.services.llm_service import llm_service
from app.prompts.legal_prompts import SC_DRAFTING_SYSTEM_PROMPT, get_sc_section_prompt

from app.core.db import db_manager, COLLECTION_NAME
from app.rag.embedder import legal_embedder

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
                return []

            formatted_results = []
            for hit in search_results:
                payload = hit.payload or {}
                formatted_results.append({
                    "title": payload.get("title", "Landmark Criminal Judgment"),
                    "citation": payload.get("citation", "Citation Pending"),
                    "relevance_score": round(float(hit.score), 3),
                    "snippet": payload.get("text", "")[:350] + "...",
                    "mongo_id": payload.get("mongo_id", ""),
                    "page_number": payload.get("paragraph_number", 1)
                })

            return formatted_results
        except Exception as e:
            print(f"[SEARCH ERROR] Qdrant query error: {e}.")
            return []

    async def get_document_by_id(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves the complete document text from MongoDB (or local JSONL file fallback) for deep-linking.
        """
        # 1. Try fetching from MongoDB if active
        mongo_db = db_manager.mongo_db
        if mongo_db is not None:
            try:
                # Query MongoDB by string id or citation
                doc = mongo_db.judgments.find_one({"$or": [{"_id": doc_id}, {"id": doc_id}, {"citation": doc_id}]})
                if doc:
                    return {
                        "id": str(doc.get("_id", doc_id)),
                        "title": doc.get("title", "Case Document"),
                        "citation": doc.get("citation", "Official Citation"),
                        "court": doc.get("court", "Indian Court"),
                        "full_text": doc.get("full_text", "")
                    }
            except Exception as e:
                print(f"[MONGO FETCH ERROR] {e}")

        # 2. Offline Fallback: Scan the local JSONL dataset file directly
        try:
            import os
            import json
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            jsonl_path = os.path.join(project_root, "datasets", "processed", "nyaya_criminal_cases.jsonl")
            if os.path.exists(jsonl_path):
                with open(jsonl_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            doc = json.loads(line)
                            if str(doc.get("id")) == str(doc_id) or str(doc.get("citation")) == str(doc_id):
                                return {
                                    "id": doc.get("id"),
                                    "title": doc.get("title", "Case Document"),
                                    "citation": doc.get("citation", "Official Citation"),
                                    "court": doc.get("court", "Indian Court"),
                                    "full_text": doc.get("full_text", "")
                                }
        except Exception as e:
            print(f"[JSONL FALLBACK ERROR] {e}")

        # 3. If not found in DB or local JSONL, return empty dict
        return {}

    async def search_statutory_laws(self, laws: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Executes search on Qdrant 'laws' collection to retrieve statutory texts.
        """
        qdrant = db_manager.qdrant
        if not qdrant or not laws:
            return []

        try:
            # Combine laws into a single query string for semantic search
            query = " ".join(laws)
            query_vector = legal_embedder.embed_text(query)
            
            if hasattr(qdrant, "search"):
                search_results = qdrant.search(
                    collection_name="statutory_laws",
                    query_vector=query_vector,
                    limit=limit
                )
            else:
                response = qdrant.query_points(
                    collection_name="statutory_laws",
                    query=query_vector,
                    limit=limit
                )
                search_results = response.points

            if not search_results:
                return []

            formatted_results = []
            for hit in search_results:
                payload = hit.payload or {}
                formatted_results.append({
                    "law_code": payload.get("law_code", ""),
                    "section": payload.get("section", ""),
                    "description": payload.get("description", ""),
                    "relevance_score": round(float(hit.score), 3)
                })

            return formatted_results
        except Exception as e:
            print(f"[SEARCH ERROR] Statutory laws search error: {e}")
            return []

    async def search_criminal_records(self, suspect_details: List[dict], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves matching criminal records using the Custom Trained ML Retriever 
        (Predicts/Matches Criminal Profiles based on Offline ML Training).
        """
        if not suspect_details:
            return []

        import os
        import joblib
        
        models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        model_path = os.path.join(models_dir, "criminal_knn_model.pkl")
        vectorizer_path = os.path.join(models_dir, "criminal_vectorizer.pkl")
        data_path = os.path.join(models_dir, "criminal_data.pkl")
        
        all_matches = []
        
        # 1. Check if trained weights exist
        if not (os.path.exists(model_path) and os.path.exists(vectorizer_path) and os.path.exists(data_path)):
            print("[SEARCH WARNING] Custom ML Retriever weights not found. Run scripts/train_criminal_model.py first.")
            return []
            
        try:
            # 2. Load Trained Weights (For Faculty Requirement)
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            df = joblib.load(data_path)
            
            for suspect in suspect_details:
                name = suspect.get("name", "")
                desc = suspect.get("description", "")
                query = f"{name} {desc}"
                
                # Transform query using the trained vectorizer
                query_vec = vectorizer.transform([query])
                
                # Predict/Match criminal profile using KNN model
                distances, indices = model.kneighbors(query_vec, n_neighbors=min(limit, len(df)))
                
                for dist, idx in zip(distances[0], indices[0]):
                    record = df.iloc[idx]
                    
                    # Compute a relevance score (inverse of distance, roughly bounded 0-1)
                    relevance = max(0.0, 1.0 - float(dist))
                    
                    if relevance > 0.05: # Only include if there's some similarity
                        all_matches.append({
                            "matched_name": str(record['name']),
                            "relevance_score": round(relevance, 3),
                            "mongo_record": {
                                "name": str(record['name']),
                                "crime_type": str(record['crime_type']),
                                "mo": str(record['mo']),
                                "traits": str(record['traits']),
                                "status": str(record['status'])
                            }
                        })

            # Sort all matches by relevance descending
            all_matches.sort(key=lambda x: x["relevance_score"], reverse=True)
            return all_matches[:limit]
            
        except Exception as e:
            print(f"[SEARCH ERROR] Custom ML Retriever error: {e}")
            return []

    async def generate_supreme_court_draft(self, case_data: dict) -> Dict[str, str]:
        """
        Processes case timeline and facts through sectioned LLM prompting models.
        Compiles the 5 core Supreme Court petition sections concurrently.
        """
        facts = case_data.get("facts", "")
        offences = case_data.get("offences", "")

        sections = ["synopsis", "list_of_dates", "questions_of_law", "grounds", "prayer"]

        async def generate_single_section(sec_name: str) -> tuple[str, str]:
            prompt = get_sc_section_prompt(sec_name, facts, offences)
            completion = await llm_service.generate_completion(
                prompt=prompt,
                system_instruction=SC_DRAFTING_SYSTEM_PROMPT
            )
            return sec_name, completion

        # Generate all 5 sections concurrently for high performance
        results = await asyncio.gather(*[generate_single_section(sec) for sec in sections])
        return dict(results)

    async def process_document_ingestion(self, doc_id: str, text: str) -> bool:
        """
        Splits text, calls embedding APIs, and updates indexes in Qdrant and MongoDB.
        """
        # TODO: Implement recursive text splitting and batch vector updates
        print(f"[AI SERVICE] Async Ingesting {doc_id} with {len(text)} characters of text.")
        return True

# Singleton instance for route imports
ai_service = AIService()
