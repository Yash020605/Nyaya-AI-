import os
import re
import json
import logging
import shutil
import pymupdf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BNSS_PDF_SOURCE = r"C:\Users\Yash\.gemini\antigravity\brain\10c21e32-d511-4f06-ba9d-3b86614f00b9\.user_uploaded\media_1791820226527_7edf5b01.pdf"

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace('\u2014', '—').replace('\u2013', '–').replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\xa0', ' ').replace('\uf02a', '').replace('\uf0be', '—')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def process_bnss_pdf():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    target_raw_pdf = os.path.join(raw_dir, "bnss_2023.pdf")
    if os.path.exists(BNSS_PDF_SOURCE) and not os.path.exists(target_raw_pdf):
        logger.info(f"Preserving BNSS PDF in {target_raw_pdf}...")
        shutil.copy2(BNSS_PDF_SOURCE, target_raw_pdf)
        
    pdf_path = target_raw_pdf if os.path.exists(target_raw_pdf) else BNSS_PDF_SOURCE
    doc = pymupdf.open(pdf_path)
    logger.info(f"Loaded BNSS PDF with {len(doc)} pages.")

    sections = {}
    titles_by_sec = {}
    current_sec = None
    current_chunks = []

    sec_start_regex = re.compile(r'(?:^|\n)\s*(\d+[A-Z]*)\.\s+')

    def is_margin(b, is_odd):
        # b: (x0, y0, x1, y1, text, block_no, block_type)
        if b[1] < 65 or b[3] > 765:
            return 'header_footer'
        if is_odd and b[0] >= 475:
            return 'margin'
        if (not is_odd) and b[2] <= 118:
            return 'margin'
        return 'body'

    # Sections 1 to 531 reside on pages 1 to 156 (index 0 to 155)
    for p in range(156):
        is_odd = ((p + 1) % 2 != 0)
        blocks = doc[p].get_text('blocks')
        blocks = sorted(blocks, key=lambda b: b[1])

        body_blocks = [b for b in blocks if is_margin(b, is_odd) == 'body']
        margin_blocks = [b for b in blocks if is_margin(b, is_odd) == 'margin']

        for b in body_blocks:
            text = b[4]
            parts = sec_start_regex.split(text)

            if len(parts) == 1:
                if current_sec is not None:
                    current_chunks.append(text)
            else:
                if parts[0] and current_sec is not None:
                    current_chunks.append(parts[0])

                for i in range(1, len(parts), 2):
                    if current_sec is not None:
                        sections[current_sec] = clean_text(''.join(current_chunks))
                    current_sec = parts[i]
                    current_chunks = [parts[i + 1]]

                    # Match closest margin note for title
                    closest_m = None
                    min_dist = 9999
                    for mb in margin_blocks:
                        dist = abs(mb[1] - b[1])
                        if dist < min_dist and dist < 65:
                            min_dist = dist
                            closest_m = mb
                    if closest_m:
                        t = ' '.join(closest_m[4].split()).strip()
                        if not re.match(r'^\d+\s+of\s+\d+\.?$', t):
                            titles_by_sec[current_sec] = clean_text(t)

    if current_sec is not None:
        sections[current_sec] = clean_text(''.join(current_chunks))

    logger.info(f"Extracted {len(sections)} sections from BNSS 2023.")

    records = []
    # Sort numerically
    sorted_keys = sorted(sections.keys(), key=lambda k: (int(re.match(r'^\d+', k).group()), k))

    for sec_num in sorted_keys:
        sec_content = sections[sec_num]
        title = titles_by_sec.get(sec_num, f"Section {sec_num} of BNSS 2023")
        doc_id = f"bnss_sec_{sec_num.lower()}"
        
        full_content = f"Section {sec_num}. {title}\n{sec_content}"
        
        record = {
            "doc_id": doc_id,
            "content": full_content,
            "doc_type": "statute",
            "metadata": {
                "act_name": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
                "section_number": sec_num,
                "title": title,
                "part": "Criminal Procedure Code 2023",
                "source_edition": "The Gazette of India Extraordinary (No. 46 of 2023)"
            }
        }
        records.append(record)

    # Write to bnss_master.jsonl
    bnss_jsonl = os.path.join(processed_dir, "bnss_master.jsonl")
    with open(bnss_jsonl, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    logger.info(f"Saved {len(records)} BNSS sections to {bnss_jsonl}")

    # Merge into statutes_master.jsonl
    statutes_jsonl = os.path.join(processed_dir, "statutes_master.jsonl")
    existing_records = []
    if os.path.exists(statutes_jsonl):
        with open(statutes_jsonl, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        existing_records.append(json.loads(line))
                    except Exception:
                        pass
                        
    existing_non_bnss = [r for r in existing_records if not r.get("doc_id", "").startswith("bnss_")]
    merged_records = existing_non_bnss + records

    with open(statutes_jsonl, "w", encoding="utf-8") as f:
        for r in merged_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    logger.info(f"Statutes Master successfully updated! Total statutory provisions: {len(merged_records)}.")
    print(f"BNSS Ingestion Complete: {len(records)} sections extracted.")

if __name__ == "__main__":
    process_bnss_pdf()
