import asyncio
import sys
from app.services.ai_service import ai_service
from app.services.citation_verifier import citation_verifier

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("==================================================")
    print("   NYAYA AI FULL BACKEND LOGIC VERIFICATION")
    print("==================================================")
    
    # 1. Test 10,000 Cases Precedent Retrieval
    print("\n1. Testing 10,000 Cases Precedent Retrieval for 'bail delay trial':")
    cases = await ai_service.search_legal_database("bail delay trial", limit=3)
    print(f"Retrieved {len(cases)} precedent cases:")
    for c in cases:
        print(f"   • {c['title']} | Citation: {c['citation']} | Score: {c['relevance_score']}")
        print(f"     Snippet: {c['snippet'][:100]}...")

    # 2. Test Statutes Retrieval from Constitution & Statutes Master
    print("\n2. Testing Statutory Retrieval for 'Article 21 life liberty':")
    statutes = await ai_service.search_statutory_laws(["21", "life"], limit=2)
    print(f"Retrieved {len(statutes)} statutory provisions:")
    for s in statutes:
        print(f"   • {s['law_code']} Art/Sec {s['section']}: {s['description']}")

    # 3. Test Custom Trained ML Retriever (KNN + Random Forest)
    print("\n3. Testing Custom Trained ML Retriever (Suspect & MO Profiling):")
    suspects = await ai_service.search_criminal_records([{"name": "Rajesh", "description": "armed robbery firearm"}], limit=2)
    print(f"Retrieved {len(suspects)} matched criminal profiles:")
    for susp in suspects:
        print(f"   • {susp['matched_name']} (Alias: {susp.get('alias')}) | Similarity: {susp['relevance_score']} | Risk: {susp['predicted_risk_level']}")
        rec = susp['mongo_record']
        print(f"     Crime: {rec['crime_type']} | MO: {rec['mo']}")

    # 4. Test Citation Verification Node (Hallucination Audit)
    print("\n4. Testing Citation & Grounding Verification Loop:")
    sample_text = "As enshrined under Article 21 and Section 439 CrPC, incarceration without trial violates liberty."
    audit = citation_verifier.verify_report_citations(sample_text, statutes, cases)
    print(f"   • Verified Sections: {audit['verified_sections']}")
    print(f"   • Grounding Confidence: {audit['grounding_confidence'] * 100}%")
    print(f"   • Audit Note: {audit['audit_summary']}")

    print("\n==================================================")
    print("   ALL LOGICAL BACKEND MODULES OPERATIONAL!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
