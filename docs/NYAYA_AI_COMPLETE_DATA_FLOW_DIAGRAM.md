# Nyaya AI (न्याय AI): Complete Unified Data Flow Diagram (DFD)

> **Document Version:** 1.0  
> **Type:** Comprehensive System-Wide Data Flow Diagram (DFD Level 0 to Level 2 Consolidated)  
> **Scope:** End-to-end tracking of data flows across External Entities, Processing Nodes, Dual-Collection RAG Stores, Machine Learning Models, and Verification Engines.

---

## 1. Visual Master Data Flow Diagram (Mermaid)

```mermaid
flowchart TD
    %% Styling Definitions
    classDef entity fill:#1e293b,stroke:#f59e0b,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef process fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#ffffff;
    classDef store fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef audit fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#ffffff;
    classDef output fill:#312e81,stroke:#818cf8,stroke-width:2px,color:#ffffff,font-weight:bold;

    %% External Entities
    E1["👤 Practicing Advocate / Defense Counsel"]:::entity
    E2["👮 Investigating Police Officer"]:::entity
    E3["⚖️ Judicial Officer / Judge / Magistrate"]:::entity
    E4["🏛️ Legislative Gazettes & Supreme Court Records"]:::entity

    %% Data Stores
    D1[("[(D1)] Raw File & FIR Buffer Store<br>PDF / Images / Text")]:::store
    D2[("[(D2)] Extracted Entity & Case Fact Cache<br>Penal Sections, Accused Profiles, MO")]:::store
    D3[("[(D3)] Statutory Master Knowledge Base<br>BNS 2023, BNSS 2023, BSA 2023, Constitution")]:::store
    D4[("[(D4)] Qdrant Dense Vector Space<br>10,000+ Precedents (384-Dim BGE Embeddings)")]:::store
    D5[("[(D5)] Historical Criminal Registry & ML Weights<br>5,000+ Suspect Profiles, KNN & RF Models")]:::store
    D6[("[(D6)] Verified Dossiers & Petitions Archive<br>Supreme Court SLP & Marathi Bail Drafts")]:::store

    %% Processes
    P1["1.0 MULTIMODAL INGESTION & LOCAL OCR<br>• PyMuPDF In-Memory Rasterization<br>• Zero-Poppler Stream Decoding<br>• Tesseract Binary Discovery"]:::process

    P2["2.0 ENTITY PARSING & STATUTORY MAPPING<br>• Regex & LLM Entity Extraction<br>• Bidirectional Code Mapping<br>(IPC ↔ BNS 2023 | CrPC ↔ BNSS 2023)"]:::process

    subgraph Dual_Collection_RAG["3.0 DUAL-COLLECTION PARALLEL RETRIEVAL ENGINE"]
        P3A["3.1 Statutory Rules Querying<br>(Binding Legislative Mandates)"]:::process
        P3B["3.2 Dense Precedent Retrieval<br>(BGE Embedding + Qdrant Cosine Search)"]:::process
        P3C["3.3 Offline ML Suspect Profiling<br>(KNN MO Match + Random Forest Risk Prediction)"]:::process
    end

    P4["4.0 LANGGRAPH AGENTIC SYNTHESIS<br>• Stateful Multi-Actor DAG Transitions<br>• Multi-Tier LLM (Gemini 1.5 Flash / Groq Fallback)<br>• Supreme Court Order XXI & Marathi Structuring"]:::process

    P5["5.0 CITATION VERIFICATION & GROUNDING AUDIT<br>• Deterministic Set-Intersection Check<br>• Empirical Grounding Score: Cg = (|Scited ∩ Sretrieved| / |Scited|)*100%<br>• Red-Flagging Hallucinated Sections"]:::audit

    P6["6.0 DOSSIER PACKAGING & BILINGUAL OUTPUT<br>• Interactive Multi-View Dashboard<br>• Deep-Linked Judgment Viewer<br>• One-Click Court-Paper Print & Copy"]:::output

    %% Data Flow Connections
    %% Ingestion Flow
    E1 -->|Uploads Scanned FIR PDF / Image / Text| P1
    E2 -->|Uploads FIR Document & Arrest Memo| P1
    E4 -.->|Official Gazette Feeds & Judgments| D3
    E4 -.->|10,000 Landmark Case Law Judgments| D4

    P1 -->|Stores Decoded Raw Buffers| D1
    D1 -->|Streams Clean Text Buffer| P2

    %% Entity Parsing Flow
    P2 -->|Stores Structured JSON Entities| D2
    D2 -->|Feeds Penal Codes & Accused Traits| P3A
    D2 -->|Feeds Crime Narrative Query Text| P3B
    D2 -->|Feeds Accused Physical & MO Features| P3C

    %% Dual-Collection RAG Lookups
    D3 <-->|Queries Exact Articles & Statutory Safeguards| P3A
    D4 <-->|Performs Cosine Similarity Search Sim(u, v) >= 0.60| P3B
    D5 <-->|Executes KNN Distance & Random Forest Inference| P3C

    %% Context Aggregation into LangGraph
    P3A -->|Retrieved Binding Statutes| P4
    P3B -->|Retrieved Landmark Case Ratios| P4
    P3C -->|Predicted Risk Level & Historical MO Matches| P4
    D2 -->|Original Case Facts & Allegations| P4

    %% Synthesis to Verification
    P4 -->|Synthesizes Draft Legal Dossier & Petitions| P5
    D3 -.->|Ground-Truth Legislative Verification Catalog| P5

    %% Audit & Output
    P5 -->|Audited Dossier + Grounding Score Badge| P6
    P6 -->|Archives Final Verified Dossier| D6

    %% Deliverables to External Entities
    P6 ==>|Delivers Supreme Court SLP Draft & Bail Dossier| E1
    P6 ==>|Delivers Suspect Syndicate Match & Evidence Dossier| E2
    P6 ==>|Delivers Verified Legal Brief & Grounding Audit Report| E3
```

---

## 2. Tabular Traceability Matrix: Data Flows & Process Interactions

| Process ID | Process Name | Inputs | Data Stores Accessed | Processing Logic | Outputs | Destination Entity / Process |
|:---:|:---|:---|:---|:---|:---|:---|
| **1.0** | **Multimodal Ingestion & Local OCR** | Raw PDF / JPG / PNG / TXT byte streams | `D1: Raw File & FIR Buffer Store` | • In-memory byte decoding via PyMuPDF (`fitz`).<br>• Direct page rasterization to PIL images without Poppler.<br>• Local Tesseract discovery with graceful fallback. | Decoded text buffer, document metadata (page count, DPI). | Process **2.0** & `D1` |
| **2.0** | **Entity Parsing & Statutory Mapping** | Decoded text buffer from `D1` | `D2: Entity & Case Fact Cache`<br>`D3: Statutory Masters` | • Regex pattern matching for penal codes.<br>• LLM entity schema extraction (incident date, location, accused traits).<br>• Bidirectional mapping (IPC $\leftrightarrow$ BNS, CrPC $\leftrightarrow$ BNSS). | Structured JSON schema `{incident_summary, applied_laws, suspect_details}`. | Processes **3.1, 3.2, 3.3** & `D2` |
| **3.1** | **Statutory Rules Querying** *(Collection A)* | Applied penal codes & procedural requests | `D3: Statutory Master Knowledge Base` | • Exact keyword and chapter lookup across BNS 2023, BNSS 2023, and the Constitution of India.<br>• Identifies statutory safeguards (e.g., Section 35 BNSS arrest protections). | Verified legislative clauses and penalty thresholds. | Process **4.0** (LangGraph Synthesizer) |
| **3.2** | **Dense Precedent Retrieval** *(Collection B)* | Factual crime narrative string | `D4: Qdrant Dense Vector Space` | • Generates 384-dimensional query vector $\mathbf{u}$ using `BAAI/bge-small-en-v1.5`.<br>• Executes Cosine Similarity search over 10,000+ judgments: $\text{Sim}(\mathbf{u}, \mathbf{v}) \ge 0.60$. | Top-3 landmark case titles, official citations (SCC/AIR), and ratio decidendi. | Process **4.0** (LangGraph Synthesizer) |
| **3.3** | **Offline ML Suspect Profiling** | Accused age, build, weapon, crime typology | `D5: Historical Criminal Registry & ML Weights` | • Min-Max feature normalization.<br>• K-Nearest Neighbors (KNN with Cosine Metric) retrieves historical MO syndicates.<br>• Random Forest (100 Trees) predicts recidivism risk category (`Low`, `Medium`, `High`). | Matched criminal profiles, similarity scores, and flight-risk confidence percentage. | Process **4.0** (LangGraph Synthesizer) |
| **4.0** | **LangGraph Agentic Synthesis** | Aggregated context from 2.0, 3.1, 3.2, 3.3 | `D2, D3, D4, D5` | • Directed Acyclic Graph (DAG) multi-agent state coordination.<br>• Multi-tier LLM fallback (Gemini 1.5 Flash $\rightarrow$ Groq LLaMA-3.3-70B $\rightarrow$ Heuristics).<br>• Section-by-section drafting (SC Order XXI / Marathi Bail Petition). | Draft legal dossier, petition text with embedded citations. | Process **5.0** (Citation Verifier) |
| **5.0** | **Citation Verification & Grounding Audit** | Synthesized draft petition from 4.0 | `D3: Statutory Master Knowledge Base` | • Extracts all cited penal provisions $S_{\text{cited}}$.<br>• Computes set-intersection against canonical statutory masters $S_{\text{retrieved}}$:<br>$$C_g = \left( \frac{\|S_{\text{cited}} \cap S_{\text{retrieved}}\|}{\|S_{\text{cited}}\|} \right) \times 100\%$$<br>• Flags unverified/hallucinated sections for quarantine. | Grounding Confidence Score ($C_g$), list of verified sections, audit warning notes. | Process **6.0** (Dossier Packaging) |
| **6.0** | **Dossier Packaging & Bilingual Output** | Audited dossier, grounding score, precedents | `D6: Verified Dossiers & Petitions Archive` | • Renders responsive glassmorphic multi-tab views.<br>• Enables deep-linking to full judgment text with page and paragraph numbers.<br>• Provides one-click clipboard copy and court-paper print styling. | Court-ready petition, full dossier, grounding audit badge. | **Advocates, Police, Judges** |

---

## 3. Data Store Catalog

| Store ID | Name | Format / Engine | Storage Location | Contents & Purpose |
|:---:|:---|:---|:---|:---|
| **D1** | **Raw File & FIR Buffer Store** | In-Memory Bytes / Temporary Buffers | Application RAM | Holds uploaded PDF, JPG, PNG, or plaintext buffers during active session processing. |
| **D2** | **Extracted Entity Cache** | JSON / Pydantic Models | Session State Memory | Caches parsed incident facts, applied penal codes, accused physical descriptions, and timestamps. |
| **D3** | **Statutory Master Knowledge Base** | JSONL Line-Delimited Catalogs | `data/processed/statutes_master.jsonl`, `bnss_master.jsonl`, `constitution_master.jsonl` | Official legislative Gazette text of Constitution of India, BNS 2023, BNSS 2023, and IPC/CrPC cross-index. |
| **D4** | **Qdrant Dense Vector Database** | HNSW Graph Index on Local Disk / Docker | `datasets/qdrant_local_db/` (Port 6333) | 384-dimensional dense neural embeddings of 10,000+ landmark Supreme Court and High Court criminal precedents. |
| **D5** | **Historical Criminal Registry & ML Weights** | Scikit-Learn `.joblib` & JSON | `backend/app/ml_models/`, `data/processed/criminal_profiles_master.jsonl` | Trained weights for KNN suspect retriever, Random Forest risk classifier, and 5,000+ historical offender records. |
| **D6** | **Verified Dossiers & Petitions Archive** | JSON / HTML / Local Storage | Client Browser Session & MongoDB | Final compiled dossiers, audited Supreme Court Order XXI SLPs, and regional Marathi district court bail petitions. |

---

## 4. Key Architectural Highlights of this Data Flow

1. **Strict Separation of Legislative Law vs. Case Law:**  
   Notice how Process **3.1** reads exclusively from **D3 (Statutory Rules)** while Process **3.2** reads exclusively from **D4 (Precedent Vectors)**. This guarantees that legislative penal codes are never confused with judicial interpretations.
2. **Zero External Binary Failure:**  
   Data flowing from External Entities (E1/E2) into Process **1.0** never calls external OS binaries like Poppler. All pixel rasterization and memory decoding occur entirely within native Python/C PyMuPDF memory.
3. **Deterministic Gatekeeper:**  
   Synthesized data generated by the LLM in Process **4.0** *cannot reach the final user* without passing through Process **5.0 (Citation Verification Node)**. This provides an absolute, mathematical barrier against generative hallucinations.

---
*NyayaAI System Architecture — ADYPSOE Department of Artificial Intelligence & Data Science, 2026-27*
