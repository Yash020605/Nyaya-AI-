import os
import json
import logging
import re
from datasets import load_dataset

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text: str) -> str:
    """Clean the text by removing excessive whitespaces and bad characters."""
    if not isinstance(text, str):
        return ""
    # Remove excessive whitespaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Basic cleanup
    return text.strip()

def process_ipc():
    logging.info("Loading Indian Penal Code (IPC) dataset...")
    try:
        dataset = load_dataset('harshitv804/Indian_Penal_Code', split='train')
    except Exception as e:
        logging.error(f"Error loading IPC dataset: {e}")
        return []
    
    records = []
    for idx, row in enumerate(dataset):
        try:
            # Fallbacks for different possible column names
            section = str(row.get('Section', row.get('section', row.get('id', f'unknown_{idx}'))))
            title = str(row.get('Title', row.get('title', '')))
            description = str(row.get('Description', row.get('description', row.get('text', ''))))
            chapter = str(row.get('Chapter', row.get('chapter', '')))
            
            content = f"{title}. {description}".strip()
            content = clean_text(content)
            
            if not content or content == ".":
                continue
                
            doc_id = f"ipc_sec_{section.replace(' ', '_').lower()}"
            
            record = {
                "doc_id": doc_id,
                "content": content,
                "doc_type": "statute",
                "metadata": {
                    "act_name": "Indian Penal Code",
                    "section_number": section,
                    "title": title,
                    "chapter": chapter
                }
            }
            records.append(record)
        except Exception as e:
            logging.warning(f"Error processing IPC row {idx}: {e}")
    
    return records

def process_constitution():
    logging.info("Loading Indian Constitution dataset...")
    try:
        dataset = load_dataset('Sharathhebbar24/Indian-Constitution', split='train')
    except Exception as e:
        logging.error(f"Error loading Constitution dataset: {e}")
        return []
    
    records = []
    for idx, row in enumerate(dataset):
        try:
            # Fallbacks for different possible column names
            article = str(row.get('Article', row.get('article', row.get('id', f'unknown_{idx}'))))
            title = str(row.get('Title', row.get('title', '')))
            description = str(row.get('Description', row.get('description', row.get('text', ''))))
            part = str(row.get('Part', row.get('part', '')))
            
            content = f"{title}. {description}".strip()
            content = clean_text(content)
            
            if not content or content == ".":
                continue
                
            doc_id = f"const_art_{article.replace(' ', '_').lower()}"
            
            record = {
                "doc_id": doc_id,
                "content": content,
                "doc_type": "statute",
                "metadata": {
                    "act_name": "Constitution of India",
                    "article_number": article,
                    "title": title,
                    "part": part
                }
            }
            records.append(record)
        except Exception as e:
            logging.warning(f"Error processing Constitution row {idx}: {e}")
            
    return records

def main():
    # Setup output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'statutes_master.jsonl')
    
    # Process datasets
    ipc_records = process_ipc()
    const_records = process_constitution()
    
    all_records = ipc_records + const_records
    
    if not all_records:
        logging.error("No records were processed successfully. Exiting.")
        return

    # Export to JSONL
    logging.info(f"Saving {len(all_records)} records to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for record in all_records:
                f.write(json.dumps(record) + '\n')
        logging.info("Statutes ingestion completed successfully.")
    except Exception as e:
        logging.error(f"Error saving to file: {e}")

if __name__ == "__main__":
    main()
