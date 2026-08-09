import os
import sys
import uuid
import logging
from typing import List, Dict, Any

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.core.db import db_manager, COLLECTION_NAME
from app.rag.chunker import legal_chunker
from app.rag.embedder import legal_embedder
from qdrant_client.http import models as qmodels

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_indian_bail_dataset(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Loads samples from SnehaDeshmukh/IndianBailJudgments-1200 dataset on HuggingFace.
    Falls back to curated sample legal cases if offline.
    """
    logger.info("Fetching IndianBailJudgments-1200 from Hugging Face...")
    documents = []

    try:
        from datasets import load_dataset
        dataset = load_dataset("SnehaDeshmukh/IndianBailJudgments-1200", split="train", streaming=True)
        count = 0
        for row in dataset:
            if count >= limit:
                break
            
            case_text = row.get("Judgment Text", row.get("text", row.get("judgment", "")))
            if not case_text or len(str(case_text).strip()) < 50:
                continue

            court = row.get("Court", "High Court of India")
            citation = row.get("Citation", row.get("Case Number", f"2024 INSC {100 + count}"))
            title = row.get("Case Title", row.get("title", f"Criminal Case {count + 1}"))
            sections = str(row.get("IPC Sections", row.get("sections", "Section 439 CrPC"))).split(",")
            outcome = row.get("Bail Outcome", row.get("outcome", "Granted"))

            documents.append({
                "title": str(title).strip(),
                "citation": str(citation).strip(),
                "court": str(court).strip(),
                "sections": [s.strip() for s in sections if s.strip()],
                "outcome": str(outcome).strip(),
                "year": row.get("Year", 2024),
                "full_text": str(case_text).strip(),
                "dataset_source": "IndianBailJudgments-1200"
            })
            count += 1
        logger.info(f"Loaded {len(documents)} judgments from IndianBailJudgments-1200.")
    except Exception as e:
        logger.warning(f"Could not stream HuggingFace dataset directly ({e}). Loading built-in Indian criminal case corpus...")
        documents = get_curated_seed_cases()

    return documents

def get_curated_seed_cases() -> List[Dict[str, Any]]:
    """Curated landmark Indian criminal and bail cases for robust local development."""
    return [
        {
            "title": "Arnesh Kumar v. State of Bihar",
            "citation": "(2014) 8 SCC 273",
            "court": "Supreme Court of India",
            "sections": ["Section 498A IPC", "Section 41 CrPC"],
            "outcome": "Bail Directions Issued",
            "year": 2014,
            "full_text": (
                "IN THE SUPREME COURT OF INDIA\nCRIMINAL APPELLATE JURISDICTION\n\n"
                "Arnesh Kumar Appellant Versus State of Bihar & Anr. Respondents\n\n"
                "1. Arrest brings humiliation, curtails freedom and casts scars forever. Law makers know it so also the police. "
                "There is a battle between the lawmakers and the police and it seems that police has not learnt its lesson.\n\n"
                "2. Our endeavor in this judgment is to ensure that police officers do not arrest the accused unnecessarily and "
                "Magistrate do not authorise detention casually and mechanically. In cases where the offence is punishable with "
                "imprisonment for a term which may be less than seven years, Section 41 CrPC mandates that arrest is not automatic.\n\n"
                "3. We direct that all State Governments instruct police officers not to automatically arrest when a case under Section 498-A IPC "
                "is registered but to satisfy themselves about the necessity for arrest under Section 41(1)(b) CrPC checklist."
            ),
            "dataset_source": "Curated LandMark Corpus"
        },
        {
            "title": "Satender Kumar Antil v. Central Bureau of Investigation",
            "citation": "(2022) 10 SCC 51",
            "court": "Supreme Court of India",
            "sections": ["Section 437 CrPC", "Section 439 CrPC", "Section 88 CrPC"],
            "outcome": "Bail Guidelines Issued",
            "year": 2022,
            "full_text": (
                "IN THE SUPREME COURT OF INDIA\nCRIMINAL APPELLATE JURISDICTION\n\n"
                "Satender Kumar Antil Appellant Versus CBI & Anr. Respondents\n\n"
                "1. The rate of conviction in criminal cases in India is abysmally low. Jail is the rule and bail is the exception is anathema "
                "to Article 21 of the Constitution of India. Undertrials should not languish in jail indefinitely when chargesheets are filed.\n\n"
                "2. Categories of offences: Category A (offences punishable with 7 years or less), Category B (offences punishable with death/life imprisonment), "
                "Category C (offences under Special Acts like NDPS, PMLA, UAPA), Category D (economic offences).\n\n"
                "3. In Category A cases, on appearance pursuant to summons without arrest during investigation, bail applications shall be decided without "
                "remanding the accused into custody, subject to non-interference with witnesses."
            ),
            "dataset_source": "Curated LandMark Corpus"
        },
        {
            "title": "State of Rajasthan v. Balchand alias Baliya",
            "citation": "1977 AIR 2447",
            "court": "Supreme Court of India",
            "sections": ["Section 439 CrPC", "Article 21 Constitution"],
            "outcome": "Bail Granted",
            "year": 1977,
            "full_text": (
                "IN THE SUPREME COURT OF INDIA\n\n"
                "State of Rajasthan v. Balchand alias Baliya\n\n"
                "1. The basic rule of our criminal jurisprudence is bail, not jail, except where there are circumstances suggestive of fleeing from "
                "justice or thwarting the course of justice or creating other troubles in the shape of repeating offences or intimidating witnesses.\n\n"
                "2. Deprivation of freedom by pre-trial imprisonment must be based on compelling reasons when the trial is delayed."
            ),
            "dataset_source": "Curated LandMark Corpus"
        },
        {
            "title": "P. Chidambaram v. Directorate of Enforcement",
            "citation": "(2020) 13 SCC 791",
            "court": "Supreme Court of India",
            "sections": ["Section 439 CrPC", "Section 420 IPC", "PMLA"],
            "outcome": "Bail Granted",
            "year": 2019,
            "full_text": (
                "IN THE SUPREME COURT OF INDIA\nCRIMINAL APPELLATE JURISDICTION\n\n"
                "P. Chidambaram Appellant Versus Directorate of Enforcement Respondent\n\n"
                "1. Even in economic offences, custody should not be punitive prior to conviction. The triple test for bail includes:\n"
                "(a) Flight risk (whether accused is likely to abscond),\n"
                "(b) Tampering with evidence,\n"
                "(c) Influencing witnesses.\n\n"
                "2. If the documentary evidence is already in possession of the investigating agency and the accused has deep roots in society, "
                "continued incarceration under Section 439 CrPC is unnecessary."
            ),
            "dataset_source": "Curated LandMark Corpus"
        }
    ]

def ingest_documents(documents: List[Dict[str, Any]]):
    """Stores full documents into MongoDB and vectors + payloads into Qdrant."""
    logger.info(f"Starting ingestion pipeline for {len(documents)} legal cases...")

    mongo_db = db_manager.mongo_db
    qdrant = db_manager.qdrant

    all_chunks = []
    
    # 1. Store in MongoDB
    for doc in documents:
        if mongo_db is not None:
            # Upsert into MongoDB judgments collection
            res = mongo_db.judgments.update_one(
                {"citation": doc["citation"]},
                {"$set": doc},
                upsert=True
            )
            doc["id"] = str(res.upserted_id or doc.get("_id", uuid.uuid4().hex))
        else:
            doc["id"] = uuid.uuid4().hex

        # 2. Chunk document
        chunks = legal_chunker.chunk_document(doc)
        all_chunks.extend(chunks)

    logger.info(f"Extracted {len(all_chunks)} searchable chunks from {len(documents)} documents.")

    if not all_chunks:
        logger.warning("No chunks generated. Ingestion finished.")
        return

    # 3. Generate Local Embeddings
    logger.info("Generating 384-dimensional dense vectors with SentenceTransformers...")
    texts_to_embed = [c["text"] for c in all_chunks]
    vectors = legal_embedder.embed_batch(texts_to_embed)

    # 4. Upsert into Qdrant
    if qdrant:
        logger.info(f"Upserting {len(all_chunks)} vectors to Qdrant collection '{COLLECTION_NAME}'...")
        points = []
        for idx, (chunk, vector) in enumerate(zip(all_chunks, vectors)):
            points.append(qmodels.PointStruct(
                id=idx + 1,
                vector=vector,
                payload=chunk
            ))
        
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        logger.info("✅ Qdrant vector index successfully updated!")
    else:
        logger.warning("Qdrant client unavailable. Ingestion skipped vector upsert.")

    logger.info("🎉 Ingestion complete! The legal research database is now live.")

if __name__ == "__main__":
    docs = load_indian_bail_dataset(limit=25)
    ingest_documents(docs)
