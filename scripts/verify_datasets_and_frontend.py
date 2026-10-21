import requests
import json

print("=== 1. Testing Frontend on Port 3000 ===")
try:
    r_front = requests.get("http://localhost:3000/")
    print("Frontend Status:", r_front.status_code)
    assert "Load Sample Cyber FIR" not in r_front.text, "Sample FIR button still found!"
    assert "btn-load-sample-fir" not in r_front.text, "btn-load-sample-fir id still found!"
    print("SUCCESS: Load Sample Cyber FIR successfully eliminated from frontend UI.")
except Exception as e:
    print("Frontend Test Error:", e)

print("\n=== 2. Testing Backend Health on Port 8000 ===")
try:
    r_health = requests.get("http://127.0.0.1:8000/health")
    print("Backend Health Status:", r_health.status_code, r_health.json())
except Exception as e:
    print("Backend Health Error:", e)

print("\n=== 3. Testing ML Suspect Matcher on 5,000 Suspects Dataset ===")
try:
    r_ml = requests.post("http://127.0.0.1:8000/api/v1/ml-retriever/predict-and-match", json={
        "primary_crime_type": "Cyber / Financial Fraud",
        "weapon_used": "None",
        "gang_affiliation": "Organized Cyber Syndicate",
        "state": "Maharashtra",
        "build": "Medium",
        "complexion": "Fair",
        "age": 28,
        "height_cm": 175,
        "prior_convictions": 2,
        "active_warrants": 1,
        "top_k": 3
    })
    print("ML Status:", r_ml.status_code)
    ml_data = r_ml.json()
    print("Predicted Risk:", ml_data.get("predicted_risk_level"), "| Confidence:", ml_data.get("confidence"))
    suspects = ml_data.get("matched_suspects", [])
    print(f"Retrieved {len(suspects)} matching suspects:")
    for s in suspects:
        print(f"  - [{s.get('criminal_id')}] {s.get('name')} (Alias: {s.get('alias')}) | Crime: {s.get('primary_crime_type')} | State: {s.get('state')} | Similarity: {s.get('similarity_score')}")
except Exception as e:
    print("ML Retriever Error:", e)

print("\n=== 4. Testing Legal Research Precedents on 10,000 Cases ===")
try:
    r_cases = requests.get("http://127.0.0.1:8000/api/v1/research/search", params={"q": "Bail arrest Section 35 BNSS Section 41A CrPC", "limit": 3})
    print("Legal Research Status:", r_cases.status_code)
    cases_data = r_cases.json()
    results = cases_data.get("results", [])
    print(f"Retrieved {len(results)} matching precedents from 10,000 cases dataset:")
    for c in results:
        print(f"  - Case: {c.get('title')} | Citation: {c.get('citation')} | Score: {c.get('relevance_score')}")
except Exception as e:
    print("Legal Research Error:", e)

print("\n=== 5. Testing Full Multi-Agent LangGraph Pipeline ===")
try:
    fir_sample = """FIRST INFORMATION REPORT
Police Station: Cyber Crime Cell, Pune City
Offences: Section 420 IPC, Section 66D IT Act, Section 35 BNSS
Accused: Rajesh Kumar, Age 32, Male, Medium build
Incident: Accused fraudulently induced complainant to transfer money via phishing and mule bank accounts."""

    files = {"file": ("fir_incident.txt", fir_sample.encode("utf-8"), "text/plain")}
    r_pipe = requests.post("http://127.0.0.1:8000/api/v1/report/generate", files=files)
    print("Pipeline Status:", r_pipe.status_code)
    pipe_data = r_pipe.json()
    print("Extracted Laws:", pipe_data.get("extracted_entities", {}).get("applied_laws"))
    print("Matched Precedents Count:", len(pipe_data.get("case_precedents", [])))
    print("Matched Suspects Count:", len(pipe_data.get("criminal_records", [])))
    for cr in pipe_data.get("criminal_records", []):
        print(f"  - Matched Criminal: [{cr.get('criminal_id')}] {cr.get('name')} | Risk: {cr.get('predicted_risk_level')} | Similarity: {cr.get('relevance_score')}")
    print("Report Synthesis Generated:", len(pipe_data.get("comprehensive_report", "")), "chars")
    print("Evidentiary Audit Status:", pipe_data.get("citation_verification", {}).get("status"))
except Exception as e:
    print("Pipeline Error:", e)
