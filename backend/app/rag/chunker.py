import re
from typing import List, Dict, Any

class LegalChunker:
    """
    Legal Document Chunker for Indian Case Law and Statutes.
    
    Ensures that every chunk retains the case's official citation, title,
    court name, and paragraph offsets so that citations in search results
    can be verified with 100% precision.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # =====================================================================
    # 🟢 TYPE YOURSELF: Legal Document Chunking & Metadata Attachment
    #
    # Why this method exists: In legal RAG, raw text splitting alone causes 
    # lost context. Chunks must carry their parent metadata (mongo_id, citation)
    # so that search results can deep-link directly to the original document.
    #
    # Common mistake: Forgetting chunk overlap, which slices legal sentences 
    # and statutory sections right down the middle.
    # =====================================================================

    def chunk_document(self, doc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Takes a full legal document dictionary and splits it into searchable 
        chunks equipped with Qdrant payload metadata.
        """
        full_text = doc_data.get("full_text", "") or ""
        mongo_id = str(doc_data.get("_id", doc_data.get("id", "")))
        title = doc_data.get("title", "Untitled Case")
        citation = doc_data.get("citation", "Citation Unavailable")
        court = doc_data.get("court", "Indian Judiciary")
        sections = doc_data.get("sections", [])
        year = doc_data.get("year", None)

        if not full_text.strip():
            return []

        # Split text into paragraphs first (respecting judicial paragraph numbering)
        raw_paragraphs = [p.strip() for p in full_text.split("\n\n") if p.strip()]
        chunks = []
        current_chunk_words = []
        current_word_count = 0
        paragraph_index = 1

        for p in raw_paragraphs:
            words = p.split()
            if not words:
                continue

            if current_word_count + len(words) > self.chunk_size and current_chunk_words:
                chunk_text = " ".join(current_chunk_words)
                chunks.append({
                    "text": chunk_text,
                    "mongo_id": mongo_id,
                    "title": title,
                    "citation": citation,
                    "court": court,
                    "paragraph_number": paragraph_index,
                    "sections": sections,
                    "year": year
                })
                # Retain overlap words from the end of the previous chunk
                overlap_words = current_chunk_words[-self.chunk_overlap:] if len(current_chunk_words) > self.chunk_overlap else []
                current_chunk_words = overlap_words + words
                current_word_count = len(current_chunk_words)
                paragraph_index += 1
            else:
                current_chunk_words.extend(words)
                current_word_count += len(words)

        if current_chunk_words:
            chunks.append({
                "text": " ".join(current_chunk_words),
                "mongo_id": mongo_id,
                "title": title,
                "citation": citation,
                "court": court,
                "paragraph_number": paragraph_index,
                "sections": sections,
                "year": year
            })

        return chunks

# Global chunker instance
legal_chunker = LegalChunker()
