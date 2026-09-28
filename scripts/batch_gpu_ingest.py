import os
import json
import logging
import uuid
from typing import List, Dict, Any
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pymongo import MongoClient, UpdateOne

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE = 384
BATCH_SIZE = 256

def init_qdrant_collections(client: QdrantClient, collections: List[str]):
    """Initialize Qdrant collections with the proper vector size."""
    for col in collections:
        if not client.collection_exists(col):
            client.create_collection(
                collection_name=col,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
            )
            logging.info(f"Created Qdrant collection: {col}")
        else:
            logging.info(f"Qdrant collection {col} already exists.")

def init_mongo_collections(db, collections: List[str]):
    """Initialize MongoDB collections and create an index on doc_id for fast lookups."""
    for col in collections:
        db[col].create_index("doc_id", unique=True)
    logging.info("MongoDB collections initialized with doc_id indexes.")

def generate_qdrant_id(doc_id: str) -> str:
    """Generate a consistent UUID for Qdrant using the unified doc_id."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))

def ingest_batch(
    batch: List[Dict[str, Any]],
    qdrant_client: QdrantClient,
    mongo_col,
    qdrant_col_name: str,
    model: SentenceTransformer
):
    """Processes a single batch: embeds texts, upserts to Qdrant, and upserts to MongoDB."""
    contents = [record["content"] for record in batch]
    
    # 1. Generate embeddings in a single batched operation
    embeddings = model.encode(contents, batch_size=BATCH_SIZE, show_progress_bar=False)
    
    # 2. Upsert to Qdrant
    points = []
    for i, record in enumerate(batch):
        point_id = generate_qdrant_id(record["doc_id"])
        
        # Store metadata and doc_id in Qdrant (omitting full content to save vector memory)
        payload = record["metadata"].copy()
        payload["doc_id"] = record["doc_id"]
        payload["doc_type"] = record["doc_type"]
        
        points.append(
            PointStruct(
                id=point_id,
                vector=embeddings[i].tolist(),
                payload=payload
            )
        )
        
    qdrant_client.upsert(
        collection_name=qdrant_col_name,
        points=points
    )
    
    # 3. Upsert to MongoDB to maintain document parity
    mongo_operations = []
    for record in batch:
        mongo_operations.append(
            UpdateOne(
                {"doc_id": record["doc_id"]},
                {"$set": record},
                upsert=True
            )
        )
        
    if mongo_operations:
        mongo_col.bulk_write(mongo_operations)

def process_file(
    filepath: str,
    qdrant_client: QdrantClient,
    mongo_col,
    qdrant_col_name: str,
    model: SentenceTransformer
):
    """Reads a .jsonl file in batches and routes them to the ingestion function."""
    if not os.path.exists(filepath):
        logging.warning(f"File not found: {filepath}. Skipping.")
        return

    # Quickly count total lines to drive the tqdm progress bar
    with open(filepath, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
        
    logging.info(f"Processing {filepath} containing {total_lines} records...")

    batch = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in tqdm(f, total=total_lines, desc=f"Ingesting {qdrant_col_name}"):
            if not line.strip():
                continue
                
            record = json.loads(line)
            batch.append(record)
            
            # Execute batch when BATCH_SIZE is reached
            if len(batch) >= BATCH_SIZE:
                ingest_batch(batch, qdrant_client, mongo_col, qdrant_col_name, model)
                batch = []
                
        # Ingest the remaining tail end of the data
        if batch:
            ingest_batch(batch, qdrant_client, mongo_col, qdrant_col_name, model)

def main():
    logging.info("Initializing models and database clients...")
    
    # Load SentenceTransformer model
    model = SentenceTransformer(MODEL_NAME)
    
    # Connect to local Qdrant and MongoDB instances
    qdrant_client = QdrantClient(host="localhost", port=6333)
    mongo_client = MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["nyaya_ai"]
    
    # Setup database collections
    qdrant_collections = ["statutes_collection", "cases_collection"]
    init_qdrant_collections(qdrant_client, qdrant_collections)
    init_mongo_collections(mongo_db, qdrant_collections)
    
    # Define file paths
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    statutes_file = os.path.join(data_dir, 'statutes_master.jsonl')
    cases_file = os.path.join(data_dir, 'criminal_cases_master.jsonl')
    
    # 1. Ingest Statutes
    process_file(
        filepath=statutes_file,
        qdrant_client=qdrant_client,
        mongo_col=mongo_db["statutes_collection"],
        qdrant_col_name="statutes_collection",
        model=model
    )
    
    # 2. Ingest Cases
    process_file(
        filepath=cases_file,
        qdrant_client=qdrant_client,
        mongo_col=mongo_db["cases_collection"],
        qdrant_col_name="cases_collection",
        model=model
    )
    
    logging.info("Batch ingestion completed successfully for all datasets!")

if __name__ == "__main__":
    main()
