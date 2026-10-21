# NyayaAI Frontend Integration Contract & API Specification ⚖️

This document outlines the API contract, endpoint catalog, and request/response payload schemas for connecting any custom frontend (React, Next.js, Vue, Flutter, etc.) to the **NyayaAI FastAPI Backend**.

---

## 🌐 Base URL & Interactive Documentation

* **Base URL (Local Development)**: `http://localhost:8000/api/v1`
* **Swagger UI (Interactive Playground)**: `http://localhost:8000/docs`
* **ReDoc Documentation**: `http://localhost:8000/redoc`
* **Content Type**: `application/json` (unless specifying multipart uploads)

---

## 📑 Endpoints Catalog

### 1. System Health Check
Check whether the backend and connected databases (MongoDB, Qdrant) are operational.

* **Method**: `GET`
* **Path**: `/health`
* **Full URL**: `http://localhost:8000/api/v1/health`
* **Headers**: None

#### Response (`200 OK`)
```json
{
  "status": "healthy",
  "services": {
    "api": "online",
    "mongodb": "pending_connection",
    "qdrant": "pending_connection"
  }
}
```

---

### 2. Case Law & Precedent Search (Research Engine)
Searches for relevant criminal cases across Qdrant vector database and fallback web networks using semantic & hybrid search.

* **Method**: `GET`
* **Path**: `/research/search`
* **Full URL**: `http://localhost:8000/api/v1/research/search?q={query}&limit={limit}`
* **Query Parameters**:
  | Parameter | Type | Required | Default | Description |
  |---|---|---|---|---|
  | `q` | `string` | **Yes** | — | Case facts, statutory query, or legal keywords (e.g. `bail under section 439 BNSS`) |
  | `limit` | `integer` | No | `5` | Maximum number of precedent chunks to return |

#### Response (`200 OK`)
```json
{
  "query": "bail under Section 439 for economic offences",
  "results": [
    {
      "title": "State of Maharashtra v. XYZ",
      "citation": "2024 INSC 999",
      "relevance_score": 0.95,
      "snippet": "In economic offences, custody should not be punitive when investigation is complete...",
      "mongo_id": "mock_mongo_id_123",
      "page_number": 3
    }
  ]
}
```

#### Error Responses
* `400 Bad Request`: When `q` query parameter is omitted or empty.
```json
{
  "detail": "Query parameter 'q' is required"
}
```

---

### 3. Fetch Full Judgment Document (Deep-Linking)
Retrieves the complete judgment text and metadata from MongoDB when a lawyer clicks on a search result citation or badge.

* **Method**: `GET`
* **Path**: `/research/document/{doc_id}`
* **Full URL**: `http://localhost:8000/api/v1/research/document/mock_mongo_id_123`
* **Path Parameters**:
  | Parameter | Type | Required | Description |
  |---|---|---|---|
  | `doc_id` | `string` | **Yes** | MongoDB document ObjectId / identifier |

#### Response (`200 OK`)
```json
{
  "id": "mock_mongo_id_123",
  "title": "State of Maharashtra v. XYZ",
  "full_text": "IN THE SUPREME COURT OF INDIA\nCRIMINAL APPELLATE JURISDICTION...\n[Complete text of the judgment]",
  "citation": "2024 INSC 999"
}
```

---

### 4. Supreme Court Petition Drafting Compiler
Receives case facts, timeline, and statutory provisions, then compiles structured petition sections aligned with Supreme Court filing rules.

* **Method**: `POST`
* **Path**: `/drafting/draft`
* **Full URL**: `http://localhost:8000/api/v1/drafting/draft`
* **Headers**: `Content-Type: application/json`

#### Request Payload (`JSON`)
```json
{
  "facts": "The petitioner was arrested on 01/01/2026 under IPC Section 420. The High Court rejected bail without considering the clean antecedents.",
  "offences": "Section 420, 120B IPC"
}
```
* **Payload Fields**:
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `facts` | `string` | **Yes** | Detailed facts, arrest dates, and lower court history |
  | `offences` | `string` | No | Applicable sections / statutes |

#### Response (`200 OK`)
```json
{
  "status": "success",
  "drafts": {
    "synopsis": "SYNOPSIS & LIST OF DATES\nThe present Special Leave Petition is directed against...",
    "list_of_dates": "1. 01/01/2026: Petitioner arrested\n2. 15/01/2026: Bail rejected by Sessions Court...",
    "questions_of_law": "A. Whether continuous incarceration without trial violates Article 21?\nB. Whether the High Court erred in ignoring Section 439 CrPC guidelines?",
    "grounds": "GROUNDS\nA. FOR THAT the High Court failed to appreciate...\nB. FOR THAT the petitioner has deep roots in society...",
    "prayer": "PRAYER\nIn the premises aforesaid, the Petitioner most respectfully prays that this Hon'ble Court may be pleased to:\n(a) Grant regular bail..."
  }
}
```

#### Error Responses
* `400 Bad Request`: When `facts` is missing from request body.
```json
{
  "detail": "Case facts are required for drafting"
}
```

---

### 3B. Marathi District & Sessions Court Drafting (मराठी न्यायालयीन मसुदा)
Generates court-ready legal filings in formal, certified governmental Marathi for District & Sessions Courts and Magistrate Courts across Maharashtra.

* **Method**: `POST`
* **Path**: `/drafting/draft/marathi`
* **Full URL**: `http://localhost:8000/api/v1/drafting/draft/marathi`
* **Headers**: `Content-Type: application/json`

#### Request Payload (`JSON`)
```json
{
  "draft_type": "bail_application",
  "court_name": "मे. सत्र न्यायालय, पुणे",
  "applicant_name": "रमेश विलास शिंदे",
  "opponent_name": "महाराष्ट्र शासन (मार्फत शिवाजीनगर पोलीस स्टेशन)",
  "police_station": "शिवाजीनगर पोलीस स्टेशन",
  "fir_number": "गु.र.नं. १२४/२०२४",
  "sections": "भा.दं.वि. कलम ३०७, ३२४, ५०४, ५०६ / बी.एन.एस.",
  "facts": "अर्जदारास राजकीय वैमनस्यातून खोट्या गुन्ह्यात गोवण्यात आले आहे. अर्जदार प्रतिष्ठित नागरिक असून तपासात पूर्ण सहकार्य करत आहे.",
  "additional_grounds": "अर्जदारावर यापूर्वी कोणताही गुन्हा दाखल नाही. अर्जदार न्यायालयाच्या सर्व अटींचे पालन करण्यास तयार आहे."
}
```

* **Supported `draft_type` options**:
  - `bail_application` (नियमित जामीन अर्ज - Regular Bail)
  - `anticipatory_bail` (अटकपूर्व जामीन अर्ज - Anticipatory Bail)
  - `criminal_complaint` (फौजदारी तक्रार अर्ज - Private Complaint)
  - `discharge_application` (दोषमुक्ततेचा अर्ज - Discharge)
  - `affidavit` (शपथपत्र / प्रतिज्ञापत्र - Affidavit)
  - `exemption_application` (हजेरीतून सूट मिळणेबाबत अर्ज - Exemption)
  - `written_arguments` (लेखी युक्तिवाद / कैफियत - Written Arguments)

#### Response (`200 OK`)
```json
{
  "status": "success",
  "draft_type": "bail_application",
  "court_name": "मे. सत्र न्यायालय, पुणे",
  "draft_text": "मेहरबान जिल्हा व सत्र न्यायालय, पुणे यांच्या न्यायालयात...\n\nफौजदारी जामीन अर्ज क्र. ...../२०२४\n\nअर्जदार/आरोपी: रमेश विलास शिंदे...\nविरुद्ध\nसामाईक/सरकार: महाराष्ट्र शासन...\n\nयास्तव नम्र प्रार्थना आहे की..."
}
```

---

### 5. Admin Case Ingestion & Vector Indexing
Allows administrators to upload new case judgments. The backend immediately accepts the job, stores raw data in MongoDB, and spawns an asynchronous background worker to chunk, embed, and upsert vectors to Qdrant.

* **Method**: `POST`
* **Path**: `/admin/ingest`
* **Full URL**: `http://localhost:8000/api/v1/admin/ingest`
* **Headers**: `Content-Type: application/json`

#### Request Payload (`JSON`)
```json
{
  "title": "State of Gujarat v. Mahesh Kumar",
  "citation": "2026 INSC 442",
  "text": "IN THE SUPREME COURT OF INDIA...\n[Full text of the judgment]"
}
```
* **Payload Fields**:
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `title` | `string` | **Yes** | Name / Title of the case or statute |
  | `citation` | `string` | **Yes** | Official citation reference string |
  | `text` | `string` | **Yes** | Full raw text of the document |

#### Response (`202 Accepted`)
```json
{
  "message": "Ingestion task initiated successfully.",
  "mongo_id": "mongo_id_98765",
  "status": "processing"
}
```

---

## 🛡️ Error Handling Contract

All backend error responses strictly conform to FastAPI's standard format:
```json
{
  "detail": "Human-readable error description"
}
```

* **Frontend developers should inspect `response.status` and display `data.detail` to the user upon error.**

---

## 🚀 Quick Fetch Example (JavaScript / TypeScript)

```typescript
// Example: Querying the research search API
async function searchCases(query: string, limit: number = 5) {
  const response = await fetch(`http://localhost:8000/api/v1/research/search?q=${encodeURIComponent(query)}&limit=${limit}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch cases');
  }

  const data = await response.json();
  return data.results; // Array of case cards
}
```
