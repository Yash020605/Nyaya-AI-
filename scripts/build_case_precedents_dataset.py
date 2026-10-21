import os
import csv
import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

random.seed(108)

TOTAL_ROWS = 10000

# Authentic landmark case templates gathered from legal precedents
LANDMARK_BASE_CASES = [
    {
        "case_title": "Lalita Kumari v. Government of Uttar Pradesh",
        "citation": "(2014) 2 SCC 1",
        "court_name": "Supreme Court of India",
        "bench_strength": "Constitution Bench (5 Judges)",
        "year": 2014,
        "primary_offence": "Mandatory Registration of FIR / Procedural Due Process",
        "applicable_sections": "Section 154 CrPC (Section 173 BNSS)",
        "crime_category": "Procedural Criminal Law",
        "facts_template": "The petitioner's minor daughter was kidnapped. Despite approaching the police authorities, an FIR was not registered for several days, citing informal preliminary inquiries.",
        "legal_issue": "Whether police officers have discretion to conduct a preliminary inquiry before registering an FIR under Section 154 CrPC when cognizable offence is disclosed?",
        "reasoning": "The language of Section 154 CrPC is imperative. The expression 'shall be reduced to writing' leaves no scope for police discretion where information discloses commission of a cognizable offence.",
        "ratio_decidendi": "Registration of an FIR under Section 154 CrPC (Section 173 BNSS) is mandatory if the information discloses a cognizable offence. Preliminary inquiry is permissible only in exceptional cases (matrimonial, commercial fraud, medical negligence, corruption) within 7 days.",
        "decision": "Directions Issued / Law Settled",
        "tags": ["FIR", "Section 154 CrPC", "Section 173 BNSS", "Mandatory Registration", "Cognizable Offence"]
    },
    {
        "case_title": "Satender Kumar Antil v. Central Bureau of Investigation",
        "citation": "(2022) 10 SCC 51",
        "court_name": "Supreme Court of India",
        "bench_strength": "Division Bench (2 Judges)",
        "year": 2022,
        "primary_offence": "Guidelines on Bail and Pre-trial Detention",
        "applicable_sections": "Sections 437, 439 CrPC (Sections 480, 483 BNSS) & Article 21",
        "crime_category": "Bail & Personal Liberty",
        "facts_template": "Appeals arising from arbitrary arrest and rejection of regular bail across multiple High Courts where accused had not been arrested during the investigation and cooperated throughout.",
        "legal_issue": "Whether an accused who was not arrested during investigation must inevitably be remanded to judicial custody upon filing of the chargesheet?",
        "reasoning": "Imprisonment before conviction is a grave deprivation of liberty under Article 21. Overcrowding of jails by undertrials is directly caused by mechanical invocation of arrest powers without adhering to Section 41 CrPC.",
        "ratio_decidendi": "Bail is the rule, jail is an exception. When an accused was not arrested during investigation and cooperated, they need not be remanded to custody upon submission of chargesheet unless exceptional circumstances exist. Offences categorized into Categories A, B, C, D.",
        "decision": "Bail Guidelines Issued",
        "tags": ["Bail", "Section 439 CrPC", "Section 483 BNSS", "Article 21", "Undertrial Rights", "Non-custodial disposal"]
    },
    {
        "case_title": "State of Haryana v. Bhajan Lal",
        "citation": "1992 Supp (1) SCC 335",
        "court_name": "Supreme Court of India",
        "bench_strength": "Division Bench (2 Judges)",
        "year": 1992,
        "primary_offence": "Quashing of Criminal Proceedings / Prevention of Abuse of Process",
        "applicable_sections": "Section 482 CrPC (Section 528 BNSS) & Sections 161, 165 IPC",
        "crime_category": "Inherent Powers & Quashing",
        "facts_template": "A criminal complaint and FIR were lodged alleging disproportionate assets and corruption. The High Court quashed the FIR at the threshold prior to investigation.",
        "legal_issue": "What are the legal parameters and boundaries for the High Court to exercise inherent powers under Section 482 CrPC to quash an FIR?",
        "reasoning": "Inherent power should be exercised sparingly and with circumspection. If uncontroverted allegations prima facie disclose commission of a cognizable offence, investigation should not be scuttled at its inception.",
        "ratio_decidendi": "Laid down seven definitive categories where High Court can quash FIR under Section 482 CrPC (Section 528 BNSS), including where allegations even if taken at face value do not constitute an offence, or where the proceeding is manifestly attended with malafide.",
        "decision": "Principles Formulated / High Court Order Set Aside",
        "tags": ["Quashing", "Section 482 CrPC", "Section 528 BNSS", "Inherent Powers", "Abuse of Process"]
    },
    {
        "case_title": "Sushila Aggarwal v. State (NCT of Delhi)",
        "citation": "(2020) 5 SCC 1",
        "court_name": "Supreme Court of India",
        "bench_strength": "Constitution Bench (5 Judges)",
        "year": 2020,
        "primary_offence": "Anticipatory Bail Scope and Duration",
        "applicable_sections": "Section 438 CrPC (Section 482 BNSS)",
        "crime_category": "Anticipatory Bail",
        "facts_template": "Conflicting judicial opinions existed regarding whether protection granted under Section 438 CrPC should be limited to a fixed duration or continue till completion of trial.",
        "legal_issue": "Whether protection granted to a person under Section 438 CrPC should be limited to a fixed period?",
        "reasoning": "Section 438 does not contain any statutory restriction on duration. Limiting the protection would curtail personal liberty under Article 21 without legislative intent.",
        "ratio_decidendi": "Anticipatory bail granted under Section 438 CrPC (Section 482 BNSS) should not be invariably limited to a fixed time period. It ordinarily operates till the conclusion of the trial unless special conditions warrant modification.",
        "decision": "Constitution Bench Order / Protection Extended",
        "tags": ["Anticipatory Bail", "Section 438 CrPC", "Section 482 BNSS", "Duration of Bail", "Article 21"]
    },
    {
        "case_title": "Arnesh Kumar v. State of Bihar",
        "citation": "(2014) 8 SCC 273",
        "court_name": "Supreme Court of India",
        "bench_strength": "Division Bench (2 Judges)",
        "year": 2014,
        "primary_offence": "Arrest Procedures & Safeguards in Offences Punishable up to 7 Years",
        "applicable_sections": "Section 41, 41A CrPC (Section 35 BNSS) & Section 498A IPC",
        "crime_category": "Arrest Safeguards",
        "facts_template": "Anticipatory bail application in a matrimonial dispute alleging demand of dowry and harassment under Section 498A IPC.",
        "legal_issue": "Whether police officers must compulsorily follow notice requirements of Section 41A CrPC before effecting arrest in offences punishable with less than seven years imprisonment?",
        "reasoning": "Arrest causes irreparable scars on reputation and liberty. Police officers often misuse the power of arrest as a tool of harassment without verifying necessity under Section 41(1)(b).",
        "ratio_decidendi": "Police officers shall not automatically arrest when a case under Section 498A IPC or offences punishable with imprisonment up to 7 years are registered. Notice of appearance under Section 41A CrPC (Section 35(3) BNSS) must be served first. Checklist must be produced before the Magistrate.",
        "decision": "Mandatory Directions Issued",
        "tags": ["Section 41A CrPC", "Section 35 BNSS", "Notice of Appearance", "Arrest Guidelines", "Matrimonial Harassment"]
    },
    {
        "case_title": "Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal",
        "citation": "(2020) 7 SCC 1",
        "court_name": "Supreme Court of India",
        "bench_strength": "Three Judges Bench",
        "year": 2020,
        "primary_offence": "Admissibility of Electronic Records in Criminal Evidence",
        "applicable_sections": "Section 65B Indian Evidence Act, 1872 (Section 63 Bharatiya Sakshya Adhiniyam, 2023)",
        "crime_category": "Law of Evidence",
        "facts_template": "Election petition and criminal dispute where electronic video recordings stored on CDs/DVDs and pen drives were produced as secondary evidence without certificate under Section 65B(4).",
        "legal_issue": "Whether certification under Section 65B(4) is mandatory for the admissibility of electronic evidence?",
        "reasoning": "Electronic evidence is volatile and susceptible to tampering. The statutory safeguard provided in Section 65B is a complete code enacted to ensure authenticity.",
        "ratio_decidendi": "A certificate under Section 65B(4) of the Evidence Act (Section 63 BSA 2023) is a mandatory condition precedent for the admissibility of secondary electronic records in any court proceedings.",
        "decision": "Law Clarified & Applied",
        "tags": ["Electronic Evidence", "Section 65B Evidence Act", "Section 63 BSA", "Digital Records", "Cyber Evidence"]
    },
    {
        "case_title": "D.K. Basu v. State of West Bengal",
        "citation": "(1997) 1 SCC 416",
        "court_name": "Supreme Court of India",
        "bench_strength": "Division Bench (2 Judges)",
        "year": 1997,
        "primary_offence": "Custodial Violence & Arrest Guidelines",
        "applicable_sections": "Articles 21 & 22(1) Constitution of India & CrPC Sections 46, 54 (BNSS Sec 36, 53)",
        "crime_category": "Human Rights & Custodial Justice",
        "facts_template": "Public interest litigation addressing rampant custodial torture, unexplained deaths in police custody, and lack of accountability of law enforcement officers.",
        "legal_issue": "What constitutional safeguards must accompany arrest and detention to prevent custodial torture and uphold Article 21?",
        "reasoning": "Custodial violence strikes at the rule of law. The power to arrest cannot be used to degrade human dignity.",
        "ratio_decidendi": "Formulated 11 mandatory requirements during arrest: clear police identification tags, arrest memo attested by witness, right to inform family member within 8-12 hours, mandatory medical examination every 48 hours, and transmission of records to Magistrate.",
        "decision": "Mandatory National Guidelines Issued",
        "tags": ["Custodial Torture", "D.K. Basu Guidelines", "Arrest Memo", "Article 21", "Medical Examination"]
    },
    {
        "case_title": "Sharad Birdhichand Sarda v. State of Maharashtra",
        "citation": "(1984) 4 SCC 116",
        "court_name": "Supreme Court of India",
        "bench_strength": "Three Judges Bench",
        "year": 1984,
        "primary_offence": "Circumstantial Evidence Standard in Murder (Panchsheel Principles)",
        "applicable_sections": "Section 302 IPC (Section 103 BNS) & Section 3 Evidence Act",
        "crime_category": "Circumstantial Evidence / Homicide",
        "facts_template": "Death of a young bride by potassium cyanide poisoning within months of marriage. Case rested purely on circumstantial evidence without direct eyewitness testimony.",
        "legal_issue": "What is the standard of proof required to sustain a conviction for murder based solely on circumstantial evidence?",
        "reasoning": "A distance exists between 'may be true' and 'must be true'. The prosecution must travel all the way to prove guilt beyond all reasonable doubt.",
        "ratio_decidendi": "Established the 'Panchsheel' (Five Golden Principles) for circumstantial evidence: (1) Circumstances fully established, (2) Facts consistent only with hypothesis of guilt, (3) Conclusive nature, (4) Exclusion of every other hypothesis, (5) Chain of events complete with no gap.",
        "decision": "Acquittal Granted on Benefit of Doubt",
        "tags": ["Circumstantial Evidence", "Section 302 IPC", "Panchsheel", "Murder", "Benefit of Doubt"]
    },
    {
        "case_title": "Tofan Singh v. State of Tamil Nadu",
        "citation": "(2021) 4 SCC 1",
        "court_name": "Supreme Court of India",
        "bench_strength": "Three Judges Bench",
        "year": 2021,
        "primary_offence": "Confessions before Investigating Officers under NDPS Act",
        "applicable_sections": "Section 67 NDPS Act & Section 25 Evidence Act (Section 23 BSA 2023)",
        "crime_category": "Narcotics & Confessional Statements",
        "facts_template": "Accused convicted of illicit trafficking of commercial quantity of ganja/charas primarily relying upon their confessional statements recorded by officers under Section 67 NDPS Act.",
        "legal_issue": "Whether statements recorded under Section 67 of the NDPS Act can be treated as confessions admissible against the accused?",
        "reasoning": "Officers empowered under Section 53 of the NDPS Act possess extensive powers of investigation akin to police officers. Treating statements made to them as admissible confessions violates Section 25 of the Evidence Act.",
        "ratio_decidendi": "Officers invested with powers under Section 53 NDPS Act are 'police officers' within the meaning of Section 25 Evidence Act; statements recorded under Section 67 NDPS cannot be used as confessional evidence against the accused.",
        "decision": "Convictions Set Aside",
        "tags": ["NDPS Act", "Section 67 NDPS", "Confession", "Section 25 Evidence Act", "Police Powers"]
    },
    {
        "case_title": "Javed Gulam Nabi Shaikh v. State of Maharashtra",
        "citation": "2024 INSC 468",
        "court_name": "Supreme Court of India",
        "bench_strength": "Division Bench (2 Judges)",
        "year": 2024,
        "primary_offence": "Prolonged Undertrial Detention and Statutory Bail Under UAPA/PMLA",
        "applicable_sections": "UAPA Section 43D(5) & Article 21 Constitution of India",
        "crime_category": "Bail & Constitutional Remedies",
        "facts_template": "The appellant had been incarcerated as an undertrial prisoner for more than four years with charges not yet framed and 80 witnesses cited by the prosecution.",
        "legal_issue": "Whether statutory embargo on bail in special acts (UAPA/NDPS) can supersede the constitutional guarantee of speedy trial under Article 21?",
        "reasoning": "No statute can override the fundamental right to life and liberty under Article 21. If the trial cannot be completed within a reasonable timeframe, prolonged incarceration without conviction is unconstitutional.",
        "ratio_decidendi": "Statutory restrictions on bail in special statutes must give way to Article 21 where there is an inordinate delay in the trial and prolonged incarceration of the undertrial.",
        "decision": "Bail Granted",
        "tags": ["Article 21", "UAPA", "Prolonged Incarceration", "Speedy Trial", "Constitutional Bail"]
    }
]

COURTS = [
    ("Supreme Court of India", "INSC"),
    ("Bombay High Court", "BHC"),
    ("Bombay High Court (Nagpur Bench)", "BHC-NAG"),
    ("Bombay High Court (Aurangabad Bench)", "BHC-AUR"),
    ("Delhi High Court", "DHC"),
    ("Allahabad High Court", "ALHC"),
    ("Madras High Court", "MADHC"),
    ("Karnataka High Court", "KARHC"),
    ("Punjab and Haryana High Court", "PHHC"),
    ("Calcutta High Court", "CALHC"),
    ("Rajasthan High Court", "RAJHC"),
    ("Gujarat High Court", "GUJHC"),
    ("Madhya Pradesh High Court", "MPHC"),
    ("Sessions Court, Greater Mumbai", "SESS-MUM"),
    ("Sessions Court, Pune", "SESS-PUN"),
    ("District & Sessions Court, Tis Hazari, Delhi", "SESS-DEL")
]

CRIME_DOMAINS = [
    {
        "crime_type": "Regular Bail / Anticipatory Bail",
        "sections": "Section 437/439 CrPC (Section 480/483 BNSS)",
        "facts_scenarios": [
            "Accused arrested in connection with an alleged financial irregularities dispute. Investigation completed, chargesheet filed, custody no longer warranted for recovery.",
            "Accused named in FIR as conspirator based solely on disclosure statement of prime suspect. No overt act of violence attributed in CCTV footage.",
            "Bail sought on grounds of parity as co-accused identically situated was granted bail by Coordinate Bench.",
            "Applicant is a female with medical complications and two minor children; chargesheet filed and no flight risk established."
        ],
        "issues": [
            "Whether continuous detention is necessary when investigation is complete and chargesheet filed?",
            "Whether applicant is entitled to bail on the ground of parity with co-accused?",
            "Whether gravity of offence alone is a sufficient ground to deny bail when trial will take substantial time?"
        ],
        "reasoning_templates": [
            "Liberty of an individual is sanctified under Article 21. Pre-trial detention cannot be transformed into punitive incarceration.",
            "Investigation stands concluded and trial is unlikely to commence in the near future. Accused has deep roots in society and no antecedents.",
            "Co-accused facing identical allegations has already been enlarged on bail. Principle of parity squarely applies."
        ],
        "ratios": [
            "Bail is the rule and jail is an exception. In the absence of apprehension of tampering with evidence or flight risk, bail should be favorably considered.",
            "Parity in bail matters must be maintained unless distinguishing features in roles of accused are explicitly demonstrated by the prosecution."
        ],
        "decisions": ["Bail Granted with Conditions", "Anticipatory Bail Granted", "Interim Protection Made Absolute"]
    },
    {
        "crime_type": "Homicide & Culpable Homicide",
        "sections": "Section 302/304 IPC (Section 103/105 BNS)",
        "facts_scenarios": [
            "Sudden altercation between neighbors over common boundary wall resulting in fatal head injury caused by single blow with wooden pestle.",
            "Allegation of contract killing with firearms. Eyewitness identification conducted without formal Test Identification Parade (TIP).",
            "Deceased died due to burn injuries in matrimonial home within two years of marriage. Dying declaration challenged on mental fitness.",
            "Group assault leading to death of victim. Prosecution claims common intention under Section 34 IPC / Section 3(5) BNS."
        ],
        "issues": [
            "Whether the act falls under Exception 4 to Section 300 IPC (sudden fight without premeditation) reducing offence to culpable homicide not amounting to murder?",
            "Whether conviction can be solely sustained on uncorroborated testimony of interested eyewitness?",
            "Whether dying declaration was recorded following strict medical certification of compos mentis?"
        ],
        "reasoning_templates": [
            "The incident occurred on spur of moment without premeditation during a sudden quarrel. The single blow indicates absence of cruel or unusual advantage.",
            "Medical evidence reveals contradictions between ocular testimony and post-mortem findings regarding time of fatal wound infliction.",
            "Dying declaration was not certified by the attending doctor prior to recording, creating reasonable doubt as to voluntary nature."
        ],
        "ratios": [
            "When death is caused during a sudden quarrel in heat of passion without premeditation and without taking undue advantage, offence falls under Section 304 Part I/II IPC.",
            "Circumstantial evidence must form a complete chain unerringly pointing to the guilt of the accused, excluding every hypothesis of innocence."
        ],
        "decisions": ["Conviction Altered from 302 IPC to 304 Part II IPC", "Acquittal Upheld on Benefit of Doubt", "Appeal Allowed in Part"]
    },
    {
        "crime_type": "Cheating, Forgery & Economic Offences",
        "sections": "Section 420/467/468/471 IPC (Section 318/336/338/340 BNS)",
        "facts_scenarios": [
            "Allegation of forging government land revenue records and transferring public land using fabricated power of attorney.",
            "Commercial contractual dispute between private companies converted into criminal FIR under Section 420 IPC to pressurize payment.",
            "Multi-level marketing scheme collecting public deposits with promise of unrealistic monthly returns, leading to default.",
            "Banking loan availed with inflated collateral valuation certificates issued by panel surveyors."
        ],
        "issues": [
            "Whether purely civil breach of contract can be converted into criminal prosecution under Section 420 IPC?",
            "Whether fraudulent intention existed at the inception of the transaction or arose subsequently?",
            "Whether ingredients of forgery under Section 463/464 IPC are made out against the applicant?"
        ],
        "reasoning_templates": [
            "To constitute an offence under Section 420 IPC, dishonest intention must be present right from the inception of the commercial transaction.",
            "Criminal law cannot be used as an arm-twisting tool to recover civil contractual dues.",
            "The original document was neither made nor signed by the applicant; mere possession without knowledge of forgery does not satisfy Section 471 IPC."
        ],
        "ratios": [
            "A mere breach of contract does not give rise to criminal prosecution for cheating unless fraudulent or dishonest intention is shown right from beginning.",
            "Civil disputes arising from commercial contracts must not be camouflaged as criminal offences under Section 420 IPC."
        ],
        "decisions": ["Criminal Proceedings Quashed under Sec 482", "Discharge Allowed", "Bail Granted with Financial Conditions"]
    },
    {
        "crime_type": "Sexual Offences & POCSO",
        "sections": "Section 376 IPC (Section 64 BNS) & Sections 4/6 POCSO Act",
        "facts_scenarios": [
            "Prosecutrix and accused in consensual relationship for two years. FIR lodged following refusal of parents to solemnize marriage.",
            "Allegation of sexual assault on minor student. Age determination disputed between school admission register and ossification test.",
            "False promise of marriage alleged after intimate relationship. WhatsApp chats indicate mutual affection and consent."
        ],
        "issues": [
            "Whether misconception of fact under Section 90 IPC is established where relationship was consensual over extended period?",
            "Whether ossification test or school entry date takes precedence in determining juvenility of victim?",
            "Whether delay of six months in lodging FIR has been satisfactorily explained by the prosecution?"
        ],
        "reasoning_templates": [
            "Consensual sexual relationship between two consenting adults cannot be termed as rape merely because the relationship ultimately broke down.",
            "Unexplained delay of several months in lodging the FIR coupled with matrimonial negotiation material creates reasonable doubt.",
            "Documentary evidence regarding date of birth based on municipal registration prevails over disputed school admissions."
        ],
        "ratios": [
            "Breach of promise to marry does not automatically amount to rape under Section 376 IPC unless false promise was given fraudulently from inception with no intention of marriage.",
            "In consensual relationships between mature individuals, subsequent refusal of family cannot convert relationship into offence of rape."
        ],
        "decisions": ["Bail Granted", "FIR Quashed", "Conviction Set Aside"]
    },
    {
        "crime_type": "Narcotics & Psychotropic Substances",
        "sections": "Sections 8/20/21/29 NDPS Act",
        "facts_scenarios": [
            "Seizure of suspected contraband from vehicle on highway. Independent panch witnesses turned hostile during trial.",
            "Allegation of possessing intermediate quantity of contraband. Mandatory notice under Section 50 NDPS regarding search before Magistrate not complied.",
            "Inordinate delay in sending seized samples to forensic laboratory without proper seal registry in police station Malkhana."
        ],
        "issues": [
            "Whether non-compliance of Section 50 NDPS Act vitiates the recovery and trial?",
            "Whether delay in forwarding chemical analysis samples compromises the chain of custody?",
            "Whether bar under Section 37 NDPS Act is overcome when procedural safeguards are violated?"
        ],
        "reasoning_templates": [
            "Section 50 NDPS Act is mandatory. Failure to inform the suspect of statutory right to be searched before a Gazetted Officer or Magistrate is fatal to the prosecution.",
            "Break in the chain of custody from time of seizure to dispatch to FSL creates grave doubts on integrity of contraband samples.",
            "Hostile panch witnesses and absence of videography of seizure procedure in breach of statutory SOP warrants grant of bail."
        ],
        "ratios": [
            "Strict compliance with Section 50 of the NDPS Act is an imperative safeguard. Any deviation renders the search and seizure illegal.",
            "Prosecution must prove unbroken chain of custody of seized samples from seizure to laboratory analysis beyond reasonable doubt."
        ],
        "decisions": ["Bail Granted", "Accused Acquitted", "Recovery Held Illegal"]
    },
    {
        "crime_type": "Quashing of FIR & Charge-sheet (Sec 482)",
        "sections": "Section 482 CrPC (Section 528 BNSS) & Sections 498A/406 IPC",
        "facts_scenarios": [
            "Matrimonial dispute where husband and distant relatives residing in foreign countries are implicated in omnibus allegations.",
            "Criminal proceedings initiated by business competitor alleging defamation and criminal intimidation over civil trademark dispute.",
            "Parties entered into comprehensive amicable settlement agreement in Mediation Centre, praying for quashing of non-compoundable FIR."
        ],
        "issues": [
            "Whether High Court can quash non-compoundable criminal proceedings where parties have reached compromise in private dispute?",
            "Whether omnibus allegations against distant in-laws without specific roles constitute abuse of legal process?",
            "Whether continuance of criminal proceedings would serve any fruitful purpose after dispute is resolved?"
        ],
        "reasoning_templates": [
            "The dispute is overwhelmingly private and matrimonial in character. Continuation of criminal prosecution would be an abuse of the process of court.",
            "No specific acts or overt roles attributed to the petitioners; inclusion of distant relatives is an abuse of matrimonial law.",
            "The parties have resolved all differences amicably through mediation and are living peacefully; quashing prevents miscarriage of justice."
        ],
        "ratios": [
            "High Court under Section 482 CrPC (Section 528 BNSS) can quash criminal proceedings in non-compoundable offences of private nature where parties have amicably resolved disputes (Gian Singh v. State of Punjab).",
            "Omnibus allegations against family members without specific attribution are liable to be quashed to prevent vexatious harassment."
        ],
        "decisions": ["FIR and Proceedings Quashed", "Petition Allowed", "Application Disposed of with Terms"]
    }
]

PARTY_NAMES_PLAINTIFF = [
    "State of Maharashtra", "State of NCT of Delhi", "State of Uttar Pradesh", "State of Karnataka",
    "State of Gujarat", "State of Rajasthan", "State of West Bengal", "Central Bureau of Investigation (CBI)",
    "National Investigation Agency (NIA)", "Enforcement Directorate (ED)", "State of Punjab", "State of Bihar"
]

PARTY_NAMES_DEFENDANT = [
    "Rameshwar Prasad & Ors.", "Mahesh Patil & Anr.", "Vikramaditya Rathore", "Sukhdev Singh Dhillon",
    "Mohammed Tariq Qureshi", "Dr. Arvind Subramaniam", "Kavita Deshmukh", "Rajendra Kumar Agarwal",
    "Sunil Bhaskar Pawar", "Jitendra Narayan Joshi", "Balwinder Singh Sandhu", "Imran Ahmed Khan",
    "Devendra Pratap Singh", "Deepak Lalwani & Ors.", "Santosh Shankar Jadhav", "Pooja Vijay Sharma"
]

def generate_precedent_record(row_idx: int) -> dict:
    # Blend landmark real cases with procedurally rich jurisprudence
    if row_idx <= len(LANDMARK_BASE_CASES):
        base = LANDMARK_BASE_CASES[row_idx - 1]
        court_name = base["court_name"]
        year = base["year"]
        citation = base["citation"]
        title = base["case_title"]
        crime_cat = base["crime_category"]
        sections = base["applicable_sections"]
        facts = base["facts_template"]
        issue = base["legal_issue"]
        reasoning = base["reasoning"]
        ratio = base["ratio_decidendi"]
        decision = base["decision"]
        bench = base["bench_strength"]
        tags = base["tags"]
    else:
        domain = random.choice(CRIME_DOMAINS)
        court_tuple = random.choice(COURTS)
        court_name = court_tuple[0]
        court_code = court_tuple[1]
        
        year = random.randint(1985, 2024)
        doc_num = random.randint(100, 9899)
        citation = f"{year} {court_code} {doc_num}"
        
        p_name = random.choice(PARTY_NAMES_PLAINTIFF)
        d_name = random.choice(PARTY_NAMES_DEFENDANT)
        
        if random.random() < 0.5:
            title = f"{d_name} v. {p_name}"
        else:
            title = f"{p_name} v. {d_name}"
            
        crime_cat = domain["crime_type"]
        sections = domain["sections"]
        facts = random.choice(domain["facts_scenarios"])
        issue = random.choice(domain["issues"])
        reasoning = random.choice(domain["reasoning_templates"])
        ratio = random.choice(domain["ratios"])
        decision = random.choice(domain["decisions"])
        bench = random.choice(["Single Judge", "Division Bench (2 Judges)", "Full Bench (3 Judges)"])
        tags = [crime_cat.split('/')[0].strip(), "Criminal Law", court_name, f"Year {year}"]

    doc_id = f"case_prec_{row_idx:05d}"
    
    # Formulate rich content string tailored for Sentence-Transformer RAG semantic embeddings
    content = (
        f"Case Law Precedent: {title}. Citation: {citation}. Court: {court_name} ({year}). Bench: {bench}. "
        f"Category: {crime_cat}. Applicable Law & Sections: {sections}. "
        f"Factual Matrix: {facts} "
        f"Substantial Question of Law: {issue} "
        f"Judicial Reasoning: {reasoning} "
        f"Ratio Decidendi: {ratio} "
        f"Final Decision: {decision}."
    )
    
    metadata = {
        "case_id": f"PREC_{row_idx:05d}",
        "case_title": title,
        "citation": citation,
        "court_name": court_name,
        "year": year,
        "bench_strength": bench,
        "crime_category": crime_cat,
        "applicable_laws": sections,
        "facts_summary": facts,
        "legal_issues": issue,
        "court_reasoning": reasoning,
        "ratio_decidendi": ratio,
        "decision": decision,
        "tags": tags
    }
    
    return {
        "doc_id": doc_id,
        "content": content,
        "doc_type": "historical_case",
        "metadata": metadata
    }

def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    csv_file = os.path.join(raw_dir, "criminal_cases_precedents_10k.csv")
    jsonl_file = os.path.join(processed_dir, "criminal_cases_master.jsonl")
    
    logger.info(f"Generating {TOTAL_ROWS} Indian Criminal Case Precedents with full feature set...")
    
    csv_headers = [
        "doc_id", "case_id", "case_title", "citation", "court_name", "year", 
        "bench_strength", "crime_category", "applicable_laws", "facts_summary", 
        "legal_issues", "court_reasoning", "ratio_decidendi", "decision", "tags", "content"
    ]
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f_csv, \
         open(jsonl_file, "w", encoding="utf-8") as f_jsonl:
        
        writer = csv.DictWriter(f_csv, fieldnames=csv_headers)
        writer.writeheader()
        
        for i in range(1, TOTAL_ROWS + 1):
            record = generate_precedent_record(i)
            
            # Write to JSONL (Unified Schema for Qdrant & MongoDB)
            f_jsonl.write(json.dumps(record, ensure_ascii=False) + "\n")
            
            # Flatten for CSV (Tabular metadata)
            m = record["metadata"]
            csv_row = {
                "doc_id": record["doc_id"],
                "case_id": m["case_id"],
                "case_title": m["case_title"],
                "citation": m["citation"],
                "court_name": m["court_name"],
                "year": m["year"],
                "bench_strength": m["bench_strength"],
                "crime_category": m["crime_category"],
                "applicable_laws": m["applicable_laws"],
                "facts_summary": m["facts_summary"],
                "legal_issues": m["legal_issues"],
                "court_reasoning": m["court_reasoning"],
                "ratio_decidendi": m["ratio_decidendi"],
                "decision": m["decision"],
                "tags": ", ".join(m["tags"]),
                "content": record["content"]
            }
            writer.writerow(csv_row)
            
            if i % 2000 == 0:
                logger.info(f"Generated {i}/{TOTAL_ROWS} case precedents...")
                
    logger.info(f"Successfully generated {TOTAL_ROWS} cases in:")
    logger.info(f" - CSV: {csv_file}")
    logger.info(f" - JSONL: {jsonl_file}")
    print(f"Dataset complete: {TOTAL_ROWS} rows ready for Qdrant and MongoDB!")

if __name__ == "__main__":
    main()
