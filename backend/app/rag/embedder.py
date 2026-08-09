import logging
from typing import List, Union
import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "BAAI/bge-small-en-v1.5"

class LegalEmbedder:
    """
    Local Embedding Engine for Indian Legal Documents.
    Runs locally on CPU for $0 using SentenceTransformers.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading local embedding model: {self.model_name}...")
                self._model = SentenceTransformer(self.model_name)
                logger.info(f"Embedding model {self.model_name} loaded successfully.")
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Using mock embedder for development.")
                self._model = "mock"

    def embed_text(self, text: str) -> List[float]:
        """Generates a normalized 384-dimensional dense vector for a text string."""
        self._load_model()
        if self._model == "mock" or self._model is None:
            # Deterministic mock vector based on text hash for tests
            np.random.seed(abs(hash(text)) % (2**32))
            vec = np.random.randn(384).astype(float)
            vec = vec / np.linalg.norm(vec)
            return vec.tolist()

        vector = self._model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Encodes a batch of texts for high-throughput database ingestion."""
        self._load_model()
        if not texts:
            return []
        if self._model == "mock" or self._model is None:
            return [self.embed_text(t) for t in texts]

        vectors = self._model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
        return vectors.tolist()

# Global embedder instance
legal_embedder = LegalEmbedder()
