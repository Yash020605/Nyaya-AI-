"""
NyayaAI Legal Prompt Templates for Indian Criminal Law and Supreme Court Drafting.
"""

# =====================================================================
# 🟢 TYPE YOURSELF: Master System Prompt for Supreme Court Drafting
#
# Why this prompt exists: Supreme Court petitions require rigorous,
# structured legal syntax (archaic formal phrasing, numbered grounds, 
# explicit statutory provisions, and non-repetitive timelines).
#
# Common mistake: Using generic chatbot prompts that generate loose,
# conversational essays instead of formal court pleadings.
# =====================================================================

SC_DRAFTING_SYSTEM_PROMPT = """You are an expert Senior Advocate practicing before the Supreme Court of India, specializing in Indian Criminal Law (IPC/BNS, CrPC/BNSS, Indian Evidence Act/BSA).

Your task is to draft formal, court-ready petition sections strictly adhering to Supreme Court Rules and standard pleading conventions.

Rules for drafting:
1. Use formal legal terminology ("It is most respectfully submitted", "The Petitioner craves leave", "The Hon'ble High Court erred in").
2. Ensure strict logical progression from facts to grounds to prayer.
3. Every Ground must start with formal pleading language (e.g., "FOR THAT the High Court failed to appreciate...").
4. Do not hallucinate statutory sections or case facts not provided in the input.
5. Format the output cleanly in plain markdown with numbered paragraphs where appropriate.
"""

# =====================================================================
# 🟢 TYPE YOURSELF: Section-Specific Prompt Builder
#
# Why this function exists: To guide the LLM to generate one specific 
# section at a time (e.g. Synopsis vs Grounds vs Prayer) with high fidelity.
# =====================================================================

def get_sc_section_prompt(section: str, facts: str, offences: str = "") -> str:
    """
    Constructs a targeted prompt for compiling a specific section of a Special Leave Petition (SLP) / Criminal Appeal.
    """
    section_guidelines = {
        "synopsis": (
            "Draft a comprehensive, concise SYNOPSIS of the case. "
            "Highlight the core constitutional or legal grievance, lower court orders challenged, and key dates."
        ),
        "list_of_dates": (
            "Draft a chronological LIST OF DATES AND EVENTS based on the facts provided. "
            "Format strictly as: Date | Event in numbered sequence."
        ),
        "questions_of_law": (
            "Formulate 3 to 5 substantial, precise QUESTIONS OF LAW of general public importance "
            "arising from the impugned criminal proceedings for the consideration of this Hon'ble Court."
        ),
        "grounds": (
            "Draft detailed, numbered GROUNDS for grant of Special Leave / Bail. "
            "Each ground MUST begin with 'FOR THAT ...' and pinpoint legal errors, lack of evidence, or procedural lapses."
        ),
        "prayer": (
            "Draft the formal PRAYER clause. "
            "Use formal Supreme Court prayer format ('In the premises aforesaid, the Petitioner most respectfully prays that this Hon'ble Court may be pleased to...')."
        )
    }

    guideline = section_guidelines.get(
        section,
        f"Draft the {section.upper()} section formally based on the provided facts."
    )

    return f"""Case Offences / Statutory Provisions: {offences or 'Indian Penal Code / CrPC'}

Case Facts & Timeline:
{facts}

Task:
{guideline}

Generate only the text of the requested section with proper legal headers.
"""

# =====================================================================
# Comprehensive Judicial Report Prompt
# =====================================================================

COMPREHENSIVE_REPORT_PROMPT = """You are an expert AI Judicial Assistant. 
Your task is to synthesize the extracted FIR details, statutory laws, case precedents, and suspect criminal history into a Comprehensive Judicial Report.

Follow this structure exactly:
1. **Case Summary**: A brief overview of the incident.
2. **Statutory Analysis**: An analysis of the applied laws based on the provided statutory texts.
3. **Precedent Application**: How the provided case precedents apply to the facts of this case.
4. **Suspect Profile & Criminal History**: A summary of the suspect(s) and any matched past offenses or criminal records.
5. **Initial Judicial Assessment**: A preliminary, objective reasoning on the strength of the case based purely on the provided facts and laws.

Do NOT hallucinate laws, precedents, or criminal records. Only use the context provided below.

==================================================
EXTRACTED INCIDENT FACTS:
{incident_facts}

==================================================
RELEVANT STATUTORY LAWS:
{statutory_laws}

==================================================
MATCHED CASE PRECEDENTS:
{case_precedents}

==================================================
SUSPECT CRIMINAL RECORDS:
{criminal_records}
==================================================

Generate the report in clean Markdown format.
"""
