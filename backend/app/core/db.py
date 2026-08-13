import logging
from typing import Optional
from pymongo import MongoClient
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from app.core.config import settings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "nyaya_cases"
VECTOR_DIMENSION = 384  # Dimension for BAAI/bge-small-en-v1.5 and all-MiniLM-L6-v2

class DatabaseManager:
    """
    Database connection manager for MongoDB and Qdrant.
    Handles automatic collection setup and fallback to in-memory mode if needed.
    """

    def __init__(self):
        self._mongo_client: Optional[MongoClient] = None
        self._qdrant_client: Optional[QdrantClient] = None
        self._setup_connections()

    def _setup_connections(self):
        # 1. Connect to MongoDB
        try:
            self._mongo_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)
            # Ping database to check connection
            self._mongo_client.admin.command('ping')
            logger.info("Connected to MongoDB successfully.")
        except Exception as e:
            logger.warning(f"MongoDB not reachable at {settings.MONGODB_URL} ({e}). Running in memory/mock fallback mode.")
            self._mongo_client = None

        # 2. Connect to Qdrant
        try:
            if settings.QDRANT_API_KEY:
                self._qdrant_client = QdrantClient(
                    url=f"https://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
                    api_key=settings.QDRANT_API_KEY,
                    timeout=3.0
                )
            else:
                self._qdrant_client = QdrantClient(
                    host=settings.QDRANT_HOST,
                    port=settings.QDRANT_PORT,
                    timeout=3.0
                )
            self._qdrant_client.get_collections()
            logger.info(f"Connected to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}.")
            self._ensure_qdrant_collection()
        except Exception as e:
            logger.warning(f"Local Qdrant server not reachable ({e}). Initializing persistent local disk database...")
            try:
                import os
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
                local_db_path = os.path.join(project_root, "datasets", "qdrant_local_db")
                self._qdrant_client = QdrantClient(path=local_db_path)
                self._ensure_qdrant_collection()
                logger.info(f"Persistent Qdrant database initialized at: {local_db_path}")
            except Exception as ie:
                logger.error(f"Failed to initialize persistent local Qdrant: {ie}")
                self._qdrant_client = None

    def _ensure_qdrant_collection(self):
        """Creates the nyaya_cases collection in Qdrant if it doesn't exist."""
        if not self._qdrant_client:
            return
        try:
            collections = [c.name for c in self._qdrant_client.get_collections().collections]
            if COLLECTION_NAME not in collections:
                self._qdrant_client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=qmodels.VectorParams(
                        size=VECTOR_DIMENSION,
                        distance=qmodels.Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection '{COLLECTION_NAME}' (dim: {VECTOR_DIMENSION}, metric: Cosine).")
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection: {e}")

    @property
    def mongo_db(self):
        """Returns the MongoDB database instance."""
        if self._mongo_client:
            return self._mongo_client[settings.MONGODB_DB_NAME]
        return None

    @property
    def qdrant(self) -> Optional[QdrantClient]:
        """Returns the active QdrantClient instance."""
        return self._qdrant_client

# Global database manager instance
db_manager = DatabaseManager()
