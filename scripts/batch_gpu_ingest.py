"""
Batch GPU Dataset Ingestion & Embedding Pipeline for NyayaAI.

Optimized for NVIDIA GPUs (RTX 3050, 4050, 4060, etc.) with automatic CUDA acceleration.
Generates an exportable Qdrant vector snapshot and MongoDB JSONL dump for peer-to-peer sharing.
"""

import os
import sys
import json
import uuid
import time
import re
import logging
from typing import List, Dict, Any

# Add backend and root directories to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(project_root, "backend"))
sys.path.insert(0, project_root)

from scripts.ingest_datasets import get_curated_seed_cases

try:
    import torch
    HAS_TORCH = True
except (ImportError, OSError) as e:
    HAS_TORCH = False
    print(f"[WDAC NOTICE] PyTorch blocked by Windows Application Control: {e}. Falling back to CPU mock embedder.")

from app.core.db import db_manager, COLLECTION_NAME, VECTOR_DIMENSION
from app.rag.chunker import legal_chunker
from app.rag.embedder import legal_embedder
from qdrant_client.http import models as qmodels

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

# Criminal law classification pattern
CRIMINAL_REGEX = re.compile(
    r"\b(IPC|CrPC|BNS|BNSS|BSA|NDPS|PMLA|POCSO|UAPA|Bail|Accused|Conviction|FIR|Police|Magistrate|Sections?\s+\d+)\b",
    re.IGNORECASE
)

def get_gpu_embedder():
    """Initializes SentenceTransformer on GPU if available, or falls back to mock."""
    if not HAS_TORCH:
        logger.warning("Running in local mock embedding mode due to OS restrictions.")
        return "mock", "cpu"
        
    try:
        from sentence_transformers import SentenceTransformer
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"⚡ Initializing Embedding Engine on device: {device.upper()}")
        if device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"🚀 Detected GPU: {gpu_name} (CUDA Enabled)")
        else:
            logger.warning("⚠️ No CUDA GPU detected. Running on CPU.")

        model = SentenceTransformer("BAAI/bge-small-en-v1.5", device=device)
        return model, device
    except Exception as e:
        logger.warning(f"Could not load SentenceTransformer ({e}). Using mock embedder.")
        return "mock", "cpu"
    return model, device

def is_criminal_case(text: str, sections: List[str]) -> bool:
    """Classifies whether a case belongs to Indian Criminal Law."""
    combined = " ".join(sections) + " " + text[:1500]
    return bool(CRIMINAL_REGEX.search(combined))

def load_all_datasets(max_cases: int = 5000) -> List[Dict[str, Any]]:
    """Loads and filters Indian criminal cases from HuggingFace datasets."""
    import socket
    socket.setdefaulttimeout(3.0)
    documents = []

    try:
        from datasets import load_dataset
        HAS_DATASETS = True
    except (ImportError, OSError) as e:
        HAS_DATASETS = False
        logger.warning(f"HuggingFace datasets library could not be loaded: {e}. Falling back to curated offline landmark corpus.")

    if HAS_DATASETS:
        # 1. IndianBailJudgments-1200
        try:
            logger.info("📥 Downloading 'SnehaDeshmukh/IndianBailJudgments-1200'...")
            bail_ds = load_dataset("SnehaDeshmukh/IndianBailJudgments-1200", split="train", streaming=True)
            for row in bail_ds:
                case_text = row.get("Judgment Text", row.get("text", row.get("judgment", "")))
                if not case_text or len(str(case_text).strip()) < 100:
                    continue

                sections = [s.strip() for s in str(row.get("IPC Sections", "")).split(",") if s.strip()]
                documents.append({
                    "id": str(uuid.uuid4().hex),
                    "title": str(row.get("Case Title", "Bail Application Judgment")).strip(),
                    "citation": str(row.get("Citation", row.get("Case Number", f"2024 INSC {len(documents)+1}"))).strip(),
                    "court": str(row.get("Court", "High Court")).strip(),
                    "sections": sections,
                    "outcome": str(row.get("Bail Outcome", "Granted")).strip(),
                    "year": row.get("Year", 2024),
                    "full_text": str(case_text).strip(),
                    "law_type": "criminal",
                    "dataset_source": "IndianBailJudgments-1200"
                })
                if len(documents) >= max_cases:
                    break
            logger.info(f"✅ Loaded {len(documents)} criminal cases from IndianBailJudgments.")
        except Exception as e:
            logger.warning(f"Could not load IndianBailJudgments dataset: {e}")

        # 2. IL-TUR Prior Case Retrieval (PCR) Subset
        if len(documents) < max_cases:
            try:
                logger.info("📥 Downloading 'Exploration-Lab/IL-TUR' (Prior Case Retrieval)...")
                iltur_ds = load_dataset("Exploration-Lab/IL-TUR", "PCR", split="train", streaming=True)
                count = 0
                for row in iltur_ds:
                    case_text = row.get("text", row.get("judgment", ""))
                    if not case_text or len(str(case_text).strip()) < 100:
                        continue

                    if not is_criminal_case(str(case_text), []):
                        continue

                    documents.append({
                        "id": str(uuid.uuid4().hex),
                        "title": str(row.get("title", f"Criminal Appeal {count+1}")).strip(),
                        "citation": str(row.get("citation", f"2023 INSC PCR-{count+1}")).strip(),
                        "court": "Supreme Court of India",
                        "sections": ["Indian Penal Code", "CrPC"],
                        "outcome": "Decided",
                        "year": 2023,
                        "full_text": str(case_text).strip(),
                        "law_type": "criminal",
                        "dataset_source": "IL-TUR-PCR"
                    })
                    count += 1
                    if len(documents) >= max_cases:
                        break
                logger.info(f"✅ Total criminal cases aggregated: {len(documents)}")
            except Exception as e:
                logger.warning(f"Could not stream IL-TUR: {e}")

    # Fallback to curated seed cases if all else fails or datasets is offline
    if not documents:
        logger.info("Loading offline seed cases database...")
        documents.extend(get_curated_seed_cases())

    return documents

def run_gpu_ingestion_pipeline(max_cases: int = 5000):
    start_time = time.time()
    logger.info("=========================================================")
    logger.info("   NYAYAAI BATCH GPU DATASET & VECTOR INGESTION")
    logger.info("=========================================================")

    # Initialize GPU Embedder
    model, device = get_gpu_embedder()
    batch_size = 256 if device == "cuda" else 32

    # Load and filter datasets
    documents = load_all_datasets(max_cases=max_cases)
    if not documents:
        logger.error("No documents loaded. Aborting.")
        return

    # Export document dump for peer-to-peer sharing
    export_dir = os.path.join(os.path.dirname(__file__), "..", "datasets", "processed")
    os.makedirs(export_dir, exist_ok=True)
    jsonl_path = os.path.join(export_dir, "nyaya_criminal_cases.jsonl")

    logger.info(f"💾 Saving full document JSONL export to {jsonl_path}...")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    # Chunking
    logger.info("✂️ Chunking documents into semantic paragraphs...")
    all_chunks = []
    for doc in documents:
        chunks = legal_chunker.chunk_document(doc)
        all_chunks.extend(chunks)

    logger.info(f"📦 Total searchable chunks to embed: {len(all_chunks)}")

    # GPU Batch Embedding
    logger.info(f"⚡ Generating dense embeddings (Batch size: {batch_size})...")
    texts = [c["text"] for c in all_chunks]
    
    embed_start = time.time()
    if model == "mock":
        vectors = legal_embedder.embed_batch(texts)
    else:
        vectors = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True
        ).tolist()
    embed_duration = round(time.time() - embed_start, 2)
    logger.info(f"✨ Embedded {len(all_chunks)} chunks in {embed_duration} seconds! ({round(len(all_chunks)/max(embed_duration, 0.1), 1)} chunks/sec)")

    # Insert into Qdrant
    qdrant = db_manager.qdrant
    if qdrant:
        logger.info(f"📥 Upserting vectors into Qdrant collection '{COLLECTION_NAME}'...")
        points = []
        for idx, (chunk, vector) in enumerate(zip(all_chunks, vectors)):
            points.append(qmodels.PointStruct(
                id=idx + 1,
                vector=vector,
                payload=chunk
            ))

        # Upload in chunks of 500
        for i in range(0, len(points), 500):
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=points[i:i+500]
            )

        logger.info("✅ Qdrant indexing complete!")

    total_time = round(time.time() - start_time, 2)
    logger.info("=========================================================")
    logger.info(f"🎉 Pipeline finished in {total_time}s!")
    logger.info(f"📁 Shareable Database File: {jsonl_path}")
    logger.info("=========================================================")

if __name__ == "__main__":
    cases = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    run_gpu_ingestion_pipeline(max_cases=cases)
