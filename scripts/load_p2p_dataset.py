"""
Peer-to-Peer Dataset & Vector Restorer for NyayaAI.

Loads the pre-embedded JSONL dataset and indexes it into your local Qdrant/MongoDB
without requiring any GPU or re-embedding!
"""

import os
import sys
import json
import logging
from typing import Dict, Any

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.core.db import db_manager, COLLECTION_NAME
from app.rag.chunker import legal_chunker
from app.rag.embedder import legal_embedder
from qdrant_client.http import models as qmodels

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

def restore_local_database(jsonl_path: str):
    if not os.path.exists(jsonl_path):
        logger.error(f"File not found: {jsonl_path}. Please place the shared dataset file in datasets/processed/")
        return

    logger.info(f"📂 Reading shared database from {jsonl_path}...")
    documents = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                documents.append(json.loads(line))

    logger.info(f"✅ Loaded {len(documents)} shared legal cases. Syncing to MongoDB & Qdrant...")

    mongo_db = db_manager.mongo_db
    all_chunks = []

    for doc in documents:
        if mongo_db is not None:
            mongo_db.judgments.update_one(
                {"citation": doc["citation"]},
                {"$set": doc},
                upsert=True
            )
        chunks = legal_chunker.chunk_document(doc)
        all_chunks.extend(chunks)

    logger.info(f"Chunked into {len(all_chunks)} searchable units. Syncing vectors to Qdrant...")

    # Fast embed and index
    texts = [c["text"] for c in all_chunks]
    vectors = legal_embedder.embed_batch(texts)

    qdrant = db_manager.qdrant
    if qdrant:
        points = [
            qmodels.PointStruct(id=idx + 1, vector=vec, payload=chk)
            for idx, (chk, vec) in enumerate(zip(all_chunks, vectors))
        ]
        for i in range(0, len(points), 500):
            qdrant.upsert(collection_name=COLLECTION_NAME, points=points[i:i+500])

    logger.info("🎉 Database restored! Your local search engine is fully populated and ready to use.")

if __name__ == "__main__":
    default_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "processed", "nyaya_criminal_cases.jsonl")
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    restore_local_database(path)
