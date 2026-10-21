import os
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        # Initialize Sentence Transformer for embedding queries
        # (This matches the model used in batch_gpu_ingest.py)
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            logger.error(f"Failed to load sentence-transformers model: {e}")
            self.model = None

        # Connect to local Qdrant
        try:
            self.qdrant_client = QdrantClient(host="localhost", port=6333)
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.qdrant_client = None

        self.statutes_col = "statutes_collection"
        self.cases_col = "cases_collection"

    def embed_query(self, query: str) -> List[float]:
        """Convert a text query into a dense vector."""
        if not self.model:
            raise RuntimeError("Embedding model is not initialized.")
        # encode returns a numpy array, convert to list for Qdrant
        return self.model.encode(query).tolist()

    def retrieve_statutes(self, applied_laws: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves relevant statutes (IPC/BNSS) based on the applied laws extracted from the FIR.
        If specific laws are provided, we embed them as queries to find semantic matches in Qdrant.
        """
        if not self.qdrant_client:
            return []
            
        if not applied_laws:
            return []
            
        results = []
        # Query each law to get the exact text/metadata from the statutes collection
        for law in applied_laws:
            query_vector = self.embed_query(law)
            try:
                search_result = self.qdrant_client.search(
                    collection_name=self.statutes_col,
                    query_vector=query_vector,
                    limit=limit
                )
                for hit in search_result:
                    results.append({
                        "score": hit.score,
                        "metadata": hit.payload
                    })
            except Exception as e:
                logger.error(f"Qdrant search failed for statute '{law}': {e}")
                
        # Sort and deduplicate based on doc_id
        unique_results = {r['metadata'].get('doc_id'): r for r in results if 'doc_id' in r['metadata']}
        sorted_results = sorted(unique_results.values(), key=lambda x: x['score'], reverse=True)
        return sorted_results[:limit*2]

    def retrieve_case_precedents(self, incident_summary: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves historical case judgments semantically similar to the incident summary.
        """
        if not self.qdrant_client or not incident_summary:
            return []
            
        query_vector = self.embed_query(incident_summary)
        try:
            search_result = self.qdrant_client.search(
                collection_name=self.cases_col,
                query_vector=query_vector,
                limit=limit
            )
            return [{"score": hit.score, "metadata": hit.payload} for hit in search_result]
        except Exception as e:
            logger.error(f"Qdrant search failed for case precedents: {e}")
            return []

retrieval_service = RetrievalService()
