import os
import re
import json
import logging
import shutil
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SOURCE_PDF_DEFAULT = r"C:\Users\Yash\.gemini\antigravity\brain\10c21e32-d511-4f06-ba9d-3b86614f00b9\.user_uploaded\media_1791820600187_3bb7120f.pdf"

def clean_text(text: str) -> str:
    """Normalize whitespace and remove OCR replacement / footnote artifacts."""
    if not text:
        return ""
    # Normalize unicode quotes and dashes
    text = text.replace('\u2014', '—').replace('\u2013', '–').replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    # Replace non-breaking spaces or replacement glyphs
    text = text.replace('\xa0', ' ').replace('\uf02a', '').replace('\uf0be', '—')
    # Remove footnote markers like 1[ or 2[ or ]
    text = re.sub(r'(\d+)\*+', '', text)
    # Remove excessive blank spaces
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def strip_page_headers_and_footnotes(raw_text: str) -> str:
    """Removes running headers, standalone page numbers, and bottom footnotes."""
    # Footnotes start below a horizontal line of underscores
    parts = re.split(r'_{5,}', raw_text)
    main_text = parts[0] if parts else raw_text
    
    lines = main_text.split('\n')
    filtered_lines = []
    for line in lines:
        s = line.strip()
        # Drop header
        if re.search(r'THE CONSTITUTION\s+OF INDIA', s, re.IGNORECASE):
            continue
        # Drop running part headers like (Part V.—The Union)
        if re.match(r'^\(?Part\s+[A-Z0-9\.\—\-\?]+.*?\)?\s*\d*$', s, re.IGNORECASE):
            continue
        # Drop standalone page numbers (e.g., ' 252 ' or '3')
        if re.match(r'^\d+$', s):
            continue
        filtered_lines.append(line)
        
    return '\n'.join(filtered_lines)

def extract_preamble(reader: PyPDF2.PdfReader) -> dict:
    """Extract Preamble from Page 32 (0-indexed 31)."""
    raw = reader.pages[31].extract_text()
    cleaned = strip_page_headers_and_footnotes(raw)
    
    # Isolate preamble text
    m = re.search(r'PREAMBLE\s+(.*)', cleaned, re.DOTALL | re.IGNORECASE)
    body = m.group(1) if m else cleaned
    body = clean_text(body)
    
    return {
        "doc_id": "const_preamble",
        "content": f"Preamble to the Constitution of India. {body}",
        "doc_type": "statute",
        "metadata": {
            "act_name": "Constitution of India",
            "article_number": "Preamble",
            "title": "Preamble",
            "part": "Preamble",
            "source_edition": "Constitution of India (Official Diglot Edition, As on May 2022)"
        }
    }

def extract_articles(reader: PyPDF2.PdfReader) -> list:
    """Extract Articles 1 to 395 across pages 33 to 284."""
    logger.info("Extracting Articles from Pages 33 to 284...")
    
    # First, concatenate cleaned body text while tracking Part and Chapter markers
    cleaned_pages = []
    for p in range(32, 284): # pages 33 to 284 (0-indexed 32 to 283)
        raw = reader.pages[p].extract_text()
        cleaned_pages.append(strip_page_headers_and_footnotes(raw))
        
    full_body = '\n'.join(cleaned_pages)
    
    # Article heading regex
    # Matches patterns like:
    # 1. Name and territory of the Union.—
    # 21A. Right to education.—
    # 31A. Saving of laws providing for acquisition of estates, etc.—
    # [31. Compulsory acquisition of property.—Omitted.]
    article_regex = re.compile(
        r'(?:^|\n)\s*(?:(?:\d+|[*])\s*\[\s*)?(\d+[A-Z]*(?:-[A-Z]+)?)\.\s+([A-Za-z\[][^.—–—\?]+?(?:\n\s*[^.—–—\?]+?){0,2})[.—–—\?]',
        re.MULTILINE
    )
    
    matches = list(article_regex.finditer(full_body))
    logger.info(f"Identified {len(matches)} article sections in body text.")
    
    # Also track Parts to give contextual metadata
    part_regex = re.compile(r'(?:^|\n)\s*(PART\s+[IVXLCDM]+[A-Z]?)\s*\n\s*([A-Z\s,—–\-]+?)(?=\n|$)', re.MULTILINE)
    part_matches = list(part_regex.finditer(full_body))
    
    def get_part_at_index(pos: int) -> str:
        current_part = "THE CONSTITUTION OF INDIA"
        for pm in part_matches:
            if pm.start() <= pos:
                p_num = pm.group(1).strip()
                p_name = clean_text(pm.group(2))
                current_part = f"{p_num}: {p_name}"
            else:
                break
        return current_part

    records = []
    for idx, match in enumerate(matches):
        art_num = match.group(1).strip()
        raw_title = clean_text(match.group(2)).strip('[]')
        start_pos = match.start()
        end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_body)
        
        chunk_text_raw = full_body[start_pos:end_pos]
        content = clean_text(chunk_text_raw)
        
        part_name = get_part_at_index(start_pos)
        
        # Format doc_id
        doc_id = f"const_art_{art_num.lower()}"
        
        record = {
            "doc_id": doc_id,
            "content": content,
            "doc_type": "statute",
            "metadata": {
                "act_name": "Constitution of India",
                "article_number": art_num,
                "title": raw_title,
                "part": part_name,
                "source_edition": "Constitution of India (Official Diglot Edition, As on May 2022)"
            }
        }
        records.append(record)
        
    return records

def extract_schedules(reader: PyPDF2.PdfReader) -> list:
    """Extract Schedules 1 through 12 across pages 285 to 383."""
    logger.info("Extracting Schedules from Pages 285 to 383...")
    
    schedule_page_ranges = [
        ("FIRST SCHEDULE", 284, 294, "Articles 1 and 4: The States and Union Territories"),
        ("SECOND SCHEDULE", 294, 300, "Articles 59, 65, 75, 97, 125, 148, 158, 164, 186, 221: Salaries and Emoluments"),
        ("THIRD SCHEDULE", 300, 304, "Articles 75, 99, 124, 148, 164, 188, 219: Forms of Oaths or Affirmations"),
        ("FOURTH SCHEDULE", 304, 307, "Articles 4 and 80: Allocation of Seats in the Council of States"),
        ("FIFTH SCHEDULE", 307, 311, "Article 244(1): Administration and Control of Scheduled Areas and Scheduled Tribes"),
        ("SIXTH SCHEDULE", 311, 341, "Articles 244(2) and 275(1): Administration of Tribal Areas in Assam, Meghalaya, Tripura and Mizoram"),
        ("SEVENTH SCHEDULE", 341, 356, "Article 246: Union List, State List, and Concurrent List"),
        ("EIGHTH SCHEDULE", 356, 358, "Articles 344(1) and 351: Recognized Official Languages"),
        ("NINTH SCHEDULE", 358, 376, "Article 31B: Validation of certain Acts and Regulations"),
        ("TENTH SCHEDULE", 376, 380, "Articles 102(2) and 191(2): Disqualification on ground of defection"),
        ("ELEVENTH SCHEDULE", 380, 382, "Article 243G: Powers, authority and responsibilities of Panchayats"),
        ("TWELFTH SCHEDULE", 382, 383, "Article 243W: Powers, authority and responsibilities of Municipalities")
    ]
    
    records = []
    num_map = {
        "FIRST": "1", "SECOND": "2", "THIRD": "3", "FOURTH": "4",
        "FIFTH": "5", "SIXTH": "6", "SEVENTH": "7", "EIGHTH": "8",
        "NINTH": "9", "TENTH": "10", "ELEVENTH": "11", "TWELFTH": "12"
    }
    
    for name, start_p, end_p, desc in schedule_page_ranges:
        pages_text = []
        for p in range(start_p, end_p + 1):
            if p < len(reader.pages):
                raw = reader.pages[p].extract_text()
                cleaned = strip_page_headers_and_footnotes(raw)
                pages_text.append(cleaned)
                
        full_sched_text = clean_text('\n'.join(pages_text))
        prefix = name.split()[0]
        sch_num = num_map.get(prefix, prefix.lower())
        doc_id = f"const_schedule_{sch_num}"
        
        record = {
            "doc_id": doc_id,
            "content": f"{name} - {desc}.\n\n{full_sched_text}",
            "doc_type": "statute",
            "metadata": {
                "act_name": "Constitution of India",
                "schedule_number": sch_num,
                "title": f"{name} - {desc}",
                "part": "Schedules",
                "source_edition": "Constitution of India (Official Diglot Edition, As on May 2022)"
            }
        }
        records.append(record)
        
    return records

def process_constitution_pdf(pdf_path: str = None):
    """Main processing function to convert Constitution PDF to unified JSONL format."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    if not pdf_path or not os.path.exists(pdf_path):
        # Look in workspace data/raw or default user uploaded directory
        local_raw = os.path.join(project_root, "data", "raw", "constitution_of_india.pdf")
        if os.path.exists(local_raw):
            pdf_path = local_raw
        elif os.path.exists(SOURCE_PDF_DEFAULT):
            pdf_path = SOURCE_PDF_DEFAULT
        else:
            raise FileNotFoundError(f"Constitution PDF not found at {SOURCE_PDF_DEFAULT} or {local_raw}")

    # Copy to project's data/raw for persistence
    raw_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    target_raw_pdf = os.path.join(raw_dir, "constitution_of_india.pdf")
    if os.path.abspath(pdf_path) != os.path.abspath(target_raw_pdf):
        logger.info(f"Copying source PDF to {target_raw_pdf}...")
        shutil.copy2(pdf_path, target_raw_pdf)

    logger.info(f"Reading PDF from: {pdf_path}")
    reader = PyPDF2.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    logger.info(f"Total pages in document: {total_pages}")
    
    # 1. Preamble
    preamble = extract_preamble(reader)
    
    # 2. Articles (1 to 395)
    articles = extract_articles(reader)
    
    # 3. Schedules (1 to 12)
    schedules = extract_schedules(reader)
    
    all_constitution_records = [preamble] + articles + schedules
    logger.info(f"Successfully generated {len(all_constitution_records)} unified Constitution records.")
    
    # Output to data/processed/
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # 1. Save dedicated Constitution dataset
    const_jsonl_file = os.path.join(processed_dir, "constitution_master.jsonl")
    logger.info(f"Writing dedicated Constitution dataset to {const_jsonl_file}...")
    with open(const_jsonl_file, "w", encoding="utf-8") as f:
        for r in all_constitution_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    # 2. Also append/upsert to statutes_master.jsonl so Qdrant batch_gpu_ingest.py picks it up immediately
    statutes_master_file = os.path.join(processed_dir, "statutes_master.jsonl")
    logger.info(f"Merging into master statutes file at {statutes_master_file}...")
    
    existing_records = {}
    if os.path.exists(statutes_master_file):
        try:
            with open(statutes_master_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        existing_records[data["doc_id"]] = data
        except Exception as e:
            logger.warning(f"Could not read existing statutes_master.jsonl: {e}")
            
    # Add new constitution records
    for r in all_constitution_records:
        existing_records[r["doc_id"]] = r
        
    with open(statutes_master_file, "w", encoding="utf-8") as f:
        for r in existing_records.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    logger.info(f"Statutes master now contains {len(existing_records)} total statutory records.")
    return len(all_constitution_records)

if __name__ == "__main__":
    count = process_constitution_pdf()
    print(f"Extraction complete! {count} items processed.")
