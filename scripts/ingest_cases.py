import os
import json
import logging
import re
from datasets import load_dataset

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_criminal_case(text: str, metadata_vals: list) -> bool:
    """Filter for purely criminal matters based on text and metadata."""
    keywords = ["ipc", "bail", "criminal appeal", "crpc", "penal code", "code of criminal procedure"]
    
    # Check metadata values first
    for val in metadata_vals:
        if isinstance(val, str):
            val_lower = val.lower()
            for kw in keywords:
                if kw in val_lower:
                    return True
                    
    # Check body text
    if isinstance(text, str):
        text_lower = text.lower()
        for kw in keywords:
            if kw in text_lower:
                return True
                
    return False

def clean_and_chunk_text(text: str, max_chunk_length: int = 2000) -> list:
    """
    Cleans out boilerplate HTML/headers and chunks long-form judgments 
    into meaningful paragraphs or argument blocks.
    """
    if not isinstance(text, str) or not text:
        return []
        
    # Remove basic HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Split by multiple newlines to preserve logical paragraph/argument boundaries
    raw_paragraphs = re.split(r'\n{2,}', text)
    chunks = []
    
    current_chunk = ""
    for para in raw_paragraphs:
        # Clean individual paragraph
        para = re.sub(r'\s+', ' ', para).strip()
        if not para:
            continue
            
        # Group paragraphs into larger blocks based on max_chunk_length
        if len(current_chunk) + len(para) > max_chunk_length:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n" + para
            else:
                current_chunk = para
                
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def process_cases():
    logging.info("Loading InJudgements dataset (streaming mode to save memory)...")
    try:
        # Use streaming to prevent loading the entire massive dataset into memory
        dataset = load_dataset('opennyaiorg/InJudgements_dataset', split='train', streaming=True)
    except Exception as e:
        logging.error(f"Error loading cases dataset: {e}")
        return
    
    # Setup output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'criminal_cases_master.jsonl')
    
    logging.info(f"Processing cases and saving to {output_file}...")
    
    processed_count = 0
    saved_count = 0
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for row in dataset:
                processed_count += 1
                if processed_count % 1000 == 0:
                    logging.info(f"Processed {processed_count} total cases, extracted {saved_count} criminal cases so far...")
                
                try:
                    # Dataset might have different schemas, trying common column names
                    case_text = str(row.get('judgment', row.get('text', '')))
                    case_id = str(row.get('id', row.get('doc_id', f'case_{processed_count}')))
                    court = str(row.get('court', 'Unknown Court'))
                    year = str(row.get('year', row.get('date', 'Unknown Year')))
                    
                    # Filtering logic
                    if not is_criminal_case(case_text, [court, case_id]):
                        continue
                    
                    # Cleaning and chunking logic
                    chunks = clean_and_chunk_text(case_text, max_chunk_length=2000)
                    
                    if not chunks:
                        continue
                        
                    for idx, chunk in enumerate(chunks):
                        doc_id = f"case_{case_id}_chunk_{idx}"
                        
                        record = {
                            "doc_id": doc_id,
                            "content": chunk,
                            "doc_type": "historical_case",
                            "metadata": {
                                "original_case_id": case_id,
                                "court_name": court,
                                "year": year,
                                "chunk_index": idx,
                                "total_chunks": len(chunks)
                            }
                        }
                        f.write(json.dumps(record) + '\n')
                    
                    saved_count += 1
                    
                except Exception as e:
                    logging.warning(f"Error processing case row {processed_count}: {e}")
                    
        logging.info(f"Cases ingestion completed. Extracted and saved {saved_count} criminal cases out of {processed_count} total processed.")
    except Exception as e:
        logging.error(f"Error during file write operations: {e}")

def main():
    process_cases()

if __name__ == "__main__":
    main()
