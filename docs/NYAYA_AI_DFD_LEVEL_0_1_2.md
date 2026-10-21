# Nyaya AI (न्याय AI): Complete Data Flow Diagrams (Level 0, Level 1 & Level 2)

> **Document Version:** 2.0  
> **Course / Academic Year:** BE Project Stage-I / AY 2026-27  
> **Department:** Department of Artificial Intelligence & Data Science Engineering  
> **Institute:** Ajeenkya DY Patil School of Engineering, Pune  
> **Sponsoring Institute:** Ajeenkya D Y Patil Law School, Pune  

---

## 1. Level 0 DFD: Context Diagram

The **Level 0 Data Flow Diagram (Context Analysis)** models Nyaya AI as a single central system process interacting directly with external human and institutional actors.

```mermaid
flowchart LR
    %% Entity Styling
    classDef entity fill:#0f172a,stroke:#d97706,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef system fill:#1e3a8a,stroke:#38bdf8,stroke-width:3px,color:#ffffff,font-weight:bold;

    E1["👤 Practicing Advocate / Defense Counsel"]:::entity
    E2["👮 Investigating Police Officer"]:::entity
    E3["⚖️ Judicial Officer / Judge / Magistrate"]:::entity
    E4["🏛️ Legislative Gazettes & Supreme Court Repositories"]:::entity

    SYS(("0<br><br>Nyaya AI<br>Judicial Intelligence<br>& Legal Drafting<br>Platform")):::system

    %% External Inputs
    E1 -->|1. Uploads Scanned FIR / Enters Facts<br>2. Selects Petition Type (SC SLP / Marathi)| SYS
    E2 -->|1. Submits FIR & Suspect Physical Traits<br>2. Submits Crime Modus Operandi (MO)| SYS
    E4 -.->|Official Gazette Texts (BNS, BNSS, BSA)<br>& 10,000+ Landmark Court Judgments| SYS

    %% System Outputs
    SYS ==>|1. Supreme Court Order XXI Petition<br>2. Regional Marathi Bail Application<br>3. Binding Case Precedents with SCC Deep-Links| E1
    SYS ==>|1. Suspect Syndicate & Prior Conviction Matches<br>2. Recidivism Risk Level & Flight Probability| E2
    SYS ==>|1. Objective Case Dossier & Summary<br>2. Citation Verification & Grounding Score (Cg)| E3
```

---

## 2. Level 1 DFD: Major Subsystems & Data Stores

The **Level 1 Data Flow Diagram** decomposes the central process into the 5 primary functional subsystems, detailing how data flows between processes and persistent storage entities.

```mermaid
flowchart TD
    %% Styling
    classDef entity fill:#0f172a,stroke:#d97706,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef process fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#ffffff;
    classDef store fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef audit fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#ffffff;
    classDef output fill:#312e81,stroke:#818cf8,stroke-width:2px,color:#ffffff,font-weight:bold;

    %% Entities
    E1["👤 Advocate"]:::entity
    E2["👮 Police"]:::entity
    E3["⚖️ Judge"]:::entity

    %% Stores
    D1[("[(D1)] Raw FIR & File Store<br>(RAM In-Memory Buffers)")]:::store
    D2[("[(D2)] Extracted Entity Cache<br>(Parsed JSON Entities)")]:::store
    D3[("[(D3)] Statutory Knowledge Base<br>(BNS/BNSS/Constitution Masters)")]:::store
    D4[("[(D4)] Qdrant Vector DB<br>(10,000 Precedents / 384-Dim BGE)")]:::store
    D5[("[(D5)] Criminal Registry & ML Models<br>(Trained KNN & RF Models)")]:::store
    D6[("[(D6)] Verified Dossiers Archive<br>(Audited Petitions & Reports)")]:::store

    %% Level 1 Processes
    P1["1.0 DOCUMENT INGESTION & LOCAL OCR<br>• PyMuPDF In-Memory Stream Rasterization<br>• Zero-Poppler Page Rendering<br>• Tesseract Binary Discovery"]:::process

    P2["2.0 LEGAL ENTITY EXTRACTION & CODE MAPPING<br>• Regex & LLM Entity Schema Parser<br>• Dynamic IPC ↔ BNS & CrPC ↔ BNSS Cross-Map"]:::process

    P3["3.0 DUAL-COLLECTION MULTI-SOURCE RETRIEVAL<br>• 3.1 Statutory Rules Querying (D3)<br>• 3.2 Dense Precedent Vector Search (D4)<br>• 3.3 Offline ML Suspect & MO Profiling (D5)"]:::process

    P4["4.0 LANGGRAPH AGENTIC SYNTHESIS<br>• Stateful Multi-Actor DAG Pipeline<br>• Multi-Tier LLM (Gemini 1.5 Flash / Groq)<br>• Order XXI (EN) & Marathi Formatting"]:::process

    P5["5.0 CITATION VERIFICATION & GROUNDING AUDIT<br>• Deterministic Set-Intersection Check<br>• Grounding Score Cg = (|Scited ∩ Sretrieved| / |Scited|)*100%<br>• Red-Flagging Hallucinated Sections"]:::audit

    P6["6.0 DOSSIER PACKAGING & BILINGUAL OUTPUT<br>• Glassmorphic Interactive Dashboard<br>• Precedent Ratio Deep-Links<br>• One-Click Court-Paper Print & Copy"]:::output

    %% Flow Connections
    E1 -->|Uploads FIR Document / Facts| P1
    E2 -->|Uploads FIR & Suspect Details| P1

    P1 -->|Writes Decoded File Stream| D1
    D1 -->|Reads Clean Text Buffer| P2

    P2 -->|Saves Structured Entities| D2
    D2 -->|Transfers Case Narrative & Sections| P3

    %% Dual-Collection RAG Lookups
    D3 <-->|Statutory Clauses & Penal Limits| P3
    D4 <-->|Dense Cosine Search Sim >= 0.60| P3
    D5 <-->|KNN MO Similarity & RF Risk Scoring| P3

    P3 -->|Aggregated Grounded Legal Context| P4
    D2 -->|Original Case Allegations| P4

    P4 -->|Synthesizes Draft Petition & Dossier| P5
    D3 -.->|Ground-Truth Legislative Master Catalog| P5

    P5 -->|Audited Output + Grounding Score (Cg)| P6
    P6 -->|Saves Verified Record| D6

    P6 ==>|Supreme Court SLP Draft & Grounded Citations| E1
    P6 ==>|Suspect Syndicate Matches & Recidivism Profile| E2
    P6 ==>|Court-Ready Dossier & Hallucination Audit Report| E3
```

---

## 3. Level 2 DFD: Decomposed Retrieval, ML Profiling & Agentic Synthesis (Process 3.0 & 4.0)

The **Level 2 Data Flow Diagram** provides deep engineering insight into the core intelligence engine: **Process 3.0 (Dual-Collection Multi-Source Retrieval)** and **Process 4.0 (LangGraph Synthesis)**.

```mermaid
flowchart TD
    %% Styling
    classDef input fill:#0f172a,stroke:#d97706,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef subproc fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#ffffff;
    classDef store fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef audit fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#ffffff;
    classDef output fill:#312e81,stroke:#818cf8,stroke-width:2px,color:#ffffff,font-weight:bold;

    %% Input Data Cache
    D2[("[(D2)] Extracted Entity Cache<br>• Applied Penal Sections<br>• Incident Narrative<br>• Accused MO & Traits")]:::store

    %% Level 2 Sub-Processes for Process 3.0
    P31["3.1 Statutory Rules Query Engine<br>• Matches BNS 2023 & BNSS 2023 sections<br>• Evaluates Section 35 BNSS arrest notice rules<br>• Retrieves Article 21 constitutional safeguards"]:::subproc

    P32["3.2 Dense Query Vector Embedder<br>• Passes incident narrative to BAAI/bge-small-en-v1.5<br>• Generates normalized 384-dimensional dense vector u"]:::subproc

    P33["3.3 Qdrant Cosine Similarity Matcher<br>• Executes HNSW graph vector search<br>• Identifies top-3 judgments where Cosine(u, v) >= 0.60"]:::subproc

    P34["3.4 Suspect Feature Normalizer<br>• Min-Max normalizes numerical traits (age, convictions)<br>• One-hot encodes categorical MO, weapons & syndicates"]:::subproc

    P35["3.5 KNN Modus Operandi Matcher<br>• Evaluates Cosine Distance: D = 1 - (xq · xi)/(||xq|| ||xi||)<br>• Retrieves top-K historical matching offenders"]:::subproc

    P36["3.6 Random Forest Risk Classifier<br>• Evaluates feature vector across T=100 decision trees<br>• Computes class probabilities P(Y=k|x) via Gini splits<br>• Outputs risk class in {Low, Medium, High}"]:::subproc

    %% Level 2 Sub-Processes for Process 4.0
    P41["4.1 Multi-Source Context Aggregator<br>• Merges statutes, case ratios & risk profile<br>• Prepares typed LangGraph state dictionary"]:::subproc

    P42["4.2 Multi-Tier LLM Generator<br>• Formats Supreme Court Order XXI petition<br>• Translates regional Marathi district bail application<br>• Fallback: Gemini 1.5 Flash -> Groq LLaMA-3.3 -> Heuristics"]:::subproc

    P50["5.0 CITATION VERIFICATION GATEWAY<br>• Regex tokenizes cited sections Scited<br>• Set-intersection with canonical master: Cg = (|Scited ∩ Sretrieved|/|Scited|)*100%<br>• Red-flags unverified sections"]:::audit

    OUT["6.0 FORMATTED COURT PETITION & DOSSIER"]:::output

    %% Data Stores
    D3[("[(D3)] Statutory Master Catalog<br>(BNS/BNSS/Constitution)")]:::store
    D4[("[(D4)] Qdrant Vector Space<br>(10,000+ Judgments)")]:::store
    D5[("[(D5)] Criminal Registry & Weights<br>(5,000+ Profiles & .joblib)")]:::store

    %% Interconnections
    D2 -->|Applied Penal Sections| P31
    D3 <-->|Lookup Clauses & Safeguards| P31

    D2 -->|Factual Crime Narrative Text| P32
    P32 -->|384-Dim Query Vector u| P33
    D4 <-->|10k Case Chunks & SCC Citations| P33

    D2 -->|Accused Traits & Crime MO| P34
    P34 -->|Normalized Vector xq| P35
    P34 -->|Normalized Vector xq| P36
    D5 <-->|Historical Profiles & KNN Graph| P35
    D5 <-->|Trained Random Forest Weights| P36

    %% Feed to Synthesis
    P31 -->|Binding Statutory Safeguards| P41
    P33 -->|Landmark Rulings & SCC Citations| P41
    P35 -->|Matched Syndicate Profiles| P41
    P36 -->|Recidivism & Flight Risk Class| P41

    P41 -->|Fused Judicial Context State| P42
    P42 -->|Synthesized Draft Petition| P50
    D3 -.->|Canonical Statutory Master Catalog| P50

    P50 -->|Audited Petition + Grounding Score (Cg)| OUT
```

---

## 4. Formal Data Dictionary (Key Flows)

| Data Flow Name | Source | Destination | Data Composition / Schema |
|:---|:---|:---|:---|
| **Raw FIR Stream** | Advocate / Police | Process 1.0 | Unstructured byte stream (PDF, PNG, JPG, TXT), filename string, mime-type. |
| **Extracted Entity Payload** | Process 2.0 | Process 3.0 / `D2` | `{incident_summary: str, applied_laws: [str], incident_date: str, incident_location: str, suspect_details: [{name: str, description: str}]}` |
| **BNS Cross-Map Record** | Process 2.0 | Process 3.1 | `{legacy_section: "420 IPC", new_section: "318 BNS", offense: "Cheating", bailability: "Cognizable / Non-Bailable", max_sentence_years: 7}` |
| **Query Embedding Vector ($\mathbf{u}$)** | Process 3.2 | Process 3.3 | Dense float32 array: $\mathbf{u} \in \mathbb{R}^{384}$, normalized $\|\mathbf{u}\|_2 = 1.0$. |
| **Precedent Record** | Process 3.3 | Process 4.1 | `{title: str, citation: "2022 10 SCC 51", relevance_score: float, ratio_decidendi: str, bench: str, page_number: int}` |
| **Suspect Risk Evaluation** | Process 3.6 | Process 4.1 | `{predicted_risk: "Low" | "Medium" | "High", confidence_score: float, matched_mo_syndicate: str, prior_convictions: int}` |
| **Grounding Audit Result** | Process 5.0 | Process 6.0 | `{grounding_confidence: 100.0%, verified_sections: ["Section 318 BNS", "Section 35 BNSS"], audit_status: "VERIFIED" | "FLAGGED"}` |
| **Court Petition Output** | Process 6.0 | Advocate / Court | Multi-section legal document conforming to Supreme Court Order XXI or Marathi District Court bail petition. |

---
*NyayaAI DFD Architecture — Ajeenkya DY Patil School of Engineering, 2026-27*
