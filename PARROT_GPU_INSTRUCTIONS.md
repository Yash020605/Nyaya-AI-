# 🦜 Parrot's GPU Ingestion Guide (RTX 4050 / CUDA)

Hey Parrot! 👋 Your GPU has been commandeered for the **NyayaAI** Indian Legal Intelligence project. 

Follow these simple steps to download, filter, and embed thousands of Indian criminal case precedents on your RTX 4050.

---

## ⚡ Prerequisites
* **Python 3.10 – 3.14** installed.
* **NVIDIA GPU Drivers** active (CUDA support).
* **Git** installed.

---

## 🚀 Step-by-Step Instructions

### Step 1: Clone the Repository
Open PowerShell or Command Prompt:
```powershell
git clone https://github.com/Omkar-Tilekar/NyayaAI.git
cd NyayaAI
```

---

### Step 2: Setup Python Virtual Environment
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

---

### Step 3: Run the GPU Batch Ingestion Script
Run the batch ingestion pipeline. You can specify how many cases to embed (default is 5,000 cases):

```powershell
.\backend\venv\Scripts\python scripts/batch_gpu_ingest.py 5000
```

#### What this command does:
1. Automatically detects your **NVIDIA RTX 4050 GPU** via CUDA.
2. Downloads `IndianBailJudgments-1200` and `IL-TUR` criminal law datasets.
3. Filters for Indian Criminal Law provisions (IPC, CrPC, BNSS, Bail).
4. Splits documents into clean semantic chunks preserving citations.
5. Uses your GPU to batch-encode embeddings at ~1,500+ chunks/second using `BAAI/bge-small-en-v1.5`.
6. Generates a standalone, exportable database file at:
   📁 **`datasets/processed/nyaya_criminal_cases.jsonl`** (~15–30 MB).

---

### Step 4: Share the Generated File

Once the terminal prints `🎉 Pipeline finished!`:

1. Locate the file:
   📂 `NyayaAI/datasets/processed/nyaya_criminal_cases.jsonl`
2. Send this file to the team using any of these zero-cost P2P methods:
   * **LocalSend** (over local Wi-Fi): [localsend.org](https://localsend.org/)
   * **Wormhole** (P2P encrypted web transfer): [wormhole.app](https://wormhole.app/)
   * **Pendrive / USB / WhatsApp Document**.

Thank you for your GPU service, Parrot! ⚖️
