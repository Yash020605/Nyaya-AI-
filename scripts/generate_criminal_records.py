import os
import csv
import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Seed for reproducibility
random.seed(42)

NUM_RECORDS = 5000

FIRST_NAMES_MALE = [
    "Rajesh", "Amit", "Vikram", "Suresh", "Manoj", "Ramesh", "Deepak", "Sunil", "Anil", "Rahul",
    "Sanjay", "Vinod", "Pankaj", "Dinesh", "Mukesh", "Ravi", "Ajay", "Santosh", "Vijay", "Ashok",
    "Pradeep", "Mahesh", "Arun", "Jitendra", "Satish", "Devendra", "Kamlesh", "Harish", "Dharmendra", "Gopal",
    "Imran", "Wasim", "Arif", "Salman", "Tariq", "Sameer", "Farhan", "Rizwan", "Nasir", "Shabbir",
    "Gurpreet", "Harpreet", "Manpreet", "Jaswinder", "Balwinder", "Kuldeep", "Davinder", "Sukhwinder"
]

FIRST_NAMES_FEMALE = [
    "Pooja", "Sunita", "Anita", "Rekha", "Geeta", "Seema", "Manju", "Kavita", "Shobha", "Meena",
    "Kusum", "Neelam", "Kamla", "Shanti", "Parveen", "Shabnam", "Raziya", "Rubina", "Simran", "Kiran"
]

LAST_NAMES = [
    "Sharma", "Verma", "Yadav", "Singh", "Kumar", "Gupta", "Mishra", "Pandey", "Tiwari", "Patel",
    "Shah", "Joshi", "Chauhan", "Rathore", "Pawar", "Kadam", "Shinde", "Jadhav", "Khan", "Ansari",
    "Qureshi", "Shaikh", "Siddiqui", "Malik", "Ali", "Gill", "Dhillon", "Sandhu", "Grewal", "Das",
    "Bose", "Banerjee", "Ghosh", "Reddy", "Rao", "Nair", "Pillai", "Iyer", "Gowda", "Hegde"
]

ALIASES = [
    "Chhota", "Bhai", "Doctor", "Pandit", "Ustad", "Kalia", "Billa", "Langda", "Goli", "Shooter",
    "Master", "Baba", "Anna", "Dada", "Tiger", "Munna", "Guddu", "Kallu", "Chikna", "Seth"
]

CRIME_PROFILES = [
    {
        "crime_type": "Theft / Burglary",
        "sections": "379/380 IPC (303/305 BNS)",
        "mo_list": [
            "Night-time house breaking using iron crowbar and master keys",
            "Pickpocketing and bag lifting in crowded railway stations and bus terminals",
            "Daytime theft from parked vehicles by smashing quarter-glass",
            "Two-wheeler vehicle lifting using duplicate ignition key bypass",
            "Theft of copper wiring and transformers from agricultural fields"
        ],
        "weapons": ["None", "Iron crowbar", "Screwdriver", "Small knife"],
        "gang_types": ["Independent", "Local Gang", "Interstate Gang"],
        "risk_levels": ["Low", "Medium"]
    },
    {
        "crime_type": "Armed Robbery / Snatching",
        "sections": "392/397 IPC (309/311 BNS)",
        "mo_list": [
            "Motorcycle-borne chain and mobile snatching targeting pedestrians at night",
            "Highway armed interception of goods trucks using spike strips and firearms",
            "Interception of jewelry store couriers and looting at gunpoint",
            "Armed hold-up of fuel petrol pumps during late night shifts",
            "Targeting bank customers withdrawing large cash amounts outside branches"
        ],
        "weapons": ["Country-made pistol (Desi Katta)", "Knife/Dagger", "Iron rod", "Country revolver"],
        "gang_types": ["Local Gang", "Organized Syndicate", "Interstate Gang"],
        "risk_levels": ["High", "Medium"]
    },
    {
        "crime_type": "Extortion / Protection Racket",
        "sections": "384/386 IPC (308 BNS)",
        "mo_list": [
            "Demanding monthly protection money (Hafta) from local builders and shop owners",
            "VoIP and virtual number threatening calls to businessmen demanding ransom",
            "Sending armed associates to construction sites to stop work until extortion paid",
            "Blackmailing victims with compromised digital photographs and private chats"
        ],
        "weapons": ["Firearm/Pistol", "None", "Country-made pistol (Desi Katta)"],
        "gang_types": ["Organized Syndicate", "Local Gang", "Interstate Gang"],
        "risk_levels": ["High", "Critical"]
    },
    {
        "crime_type": "Homicide / Murder",
        "sections": "302/307 IPC (103/109 BNS)",
        "mo_list": [
            "Contract killing (Supari) executed via pillion rider firearm discharge",
            "Fatal assault during violent property dispute using sharp farming implements",
            "Targeted gang rivalry revenge killing in public transit area",
            "Premeditated poisoning staged as accidental overdose"
        ],
        "weapons": ["Country-made pistol (Desi Katta)", "Imported 9mm pistol", "Sharp cleaver/Sword", "Iron rod"],
        "gang_types": ["Organized Syndicate", "Local Gang", "Independent"],
        "risk_levels": ["Critical", "High"]
    },
    {
        "crime_type": "Assault & Grievous Hurt",
        "sections": "323/326 IPC (115/117 BNS)",
        "mo_list": [
            "Brawling and violent physical intimidation over territorial dominance",
            "Coordinated group assault armed with lathis and knuckledusters outside market",
            "Road rage altercation leading to grievous blunt-force injury"
        ],
        "weapons": ["Iron rod", "Wooden club (Lathi)", "Knuckleduster", "Pocket knife"],
        "gang_types": ["Independent", "Local Gang"],
        "risk_levels": ["Low", "Medium"]
    },
    {
        "crime_type": "Cyber Fraud & Financial Cheating",
        "sections": "420 IPC (318 BNS) & 66D IT Act",
        "mo_list": [
            "SIM swap and banking OTP phishing through malicious fake utility APKs",
            "Posing as customer care executive to initiate remote access via AnyDesk/TeamViewer",
            "Investment Ponzi and cryptocurrency telegram scam promising 200% returns",
            "Fake matrimonial profile financial extortion after emotional grooming"
        ],
        "weapons": ["None / Digital devices"],
        "gang_types": ["Interstate Gang", "Organized Syndicate", "Independent"],
        "risk_levels": ["Medium", "High"]
    },
    {
        "crime_type": "Narcotics Trafficking (NDPS)",
        "sections": "8/20/21 NDPS Act (Commercial Quantity)",
        "mo_list": [
            "Interstate trafficking of synthetic MDMA and heroin hidden in vegetable supply trucks",
            "Peddling contraband to university and night club patrons via dead drops",
            "Courier packaging concealment with forged false declaration slips"
        ],
        "weapons": ["None", "Concealed knife", "Country-made pistol (Desi Katta)"],
        "gang_types": ["Organized Syndicate", "Interstate Gang"],
        "risk_levels": ["High", "Critical"]
    },
    {
        "crime_type": "Kidnapping / Abduction",
        "sections": "364A/365 IPC (140 BNS)",
        "mo_list": [
            "Abducting children of affluent businessmen outside school gates for ransom",
            "Luring job seekers to remote locations and detaining them for ransom demands",
            "Honey-trap abduction into isolated rural farmhouses"
        ],
        "weapons": ["Firearm/Pistol", "Chloroform/Sedatives", "Country-made pistol (Desi Katta)"],
        "gang_types": ["Organized Syndicate", "Interstate Gang"],
        "risk_levels": ["Critical", "High"]
    }
]

LOCATIONS = [
    {"state": "Delhi", "district": "North West Delhi", "region": "Delhi NCR"},
    {"state": "Delhi", "district": "South East Delhi", "region": "Delhi NCR"},
    {"state": "Maharashtra", "district": "Mumbai City", "region": "Western"},
    {"state": "Maharashtra", "district": "Thane", "region": "Western"},
    {"state": "Maharashtra", "district": "Pune", "region": "Western"},
    {"state": "Uttar Pradesh", "district": "Noida / Gautam Buddha Nagar", "region": "Northern"},
    {"state": "Uttar Pradesh", "district": "Lucknow", "region": "Northern"},
    {"state": "Uttar Pradesh", "district": "Kanpur Nagar", "region": "Northern"},
    {"state": "Karnataka", "district": "Bengaluru Urban", "region": "Southern"},
    {"state": "Karnataka", "district": "Mysuru", "region": "Southern"},
    {"state": "West Bengal", "district": "Kolkata", "region": "Eastern"},
    {"state": "West Bengal", "district": "Howrah", "region": "Eastern"},
    {"state": "Telangana", "district": "Hyderabad", "region": "Southern"},
    {"state": "Gujarat", "district": "Ahmedabad", "region": "Western"},
    {"state": "Gujarat", "district": "Surat", "region": "Western"},
    {"state": "Rajasthan", "district": "Jaipur", "region": "Northern"},
    {"state": "Bihar", "district": "Patna", "region": "Eastern"},
    {"state": "Punjab", "district": "Ludhiana", "region": "Northern"},
    {"state": "Madhya Pradesh", "district": "Indore", "region": "Central"},
    {"state": "Tamil Nadu", "district": "Chennai", "region": "Southern"}
]

BUILDS = ["Lean", "Medium", "Athletic", "Heavy", "Stocky"]
COMPLEXIONS = ["Fair", "Wheatish", "Dark", "Medium"]
IDENTIFYING_MARKS = [
    "Deep scar on left cheek",
    "Tattoo of tiger on right forearm",
    "Burn mark on right side of neck",
    "Prominent mole above upper lip",
    "Noticeable limp in left leg",
    "Surgical scar on right eyebrow",
    "Tattoo of trident (Trishul) on left wrist",
    "Missing tip of right index finger",
    "Scar across bridge of nose",
    "Skull tattoo on chest",
    "Cauliflower ear on right side",
    "No distinct permanent marks"
]

def generate_record(idx: int) -> dict:
    gender = random.choices(["Male", "Female"], weights=[0.92, 0.08])[0]
    
    if gender == "Male":
        first_name = random.choice(FIRST_NAMES_MALE)
    else:
        first_name = random.choice(FIRST_NAMES_FEMALE)
        
    last_name = random.choice(LAST_NAMES)
    full_name = f"{first_name} {last_name}"
    
    # 65% chance of having a known alias
    if random.random() < 0.65:
        alias = f"{random.choice(ALIASES)} {first_name}"
    else:
        alias = "None"
        
    age = random.randint(19, 58)
    
    profile = random.choice(CRIME_PROFILES)
    crime_type = profile["crime_type"]
    applied_sections = profile["sections"]
    mo = random.choice(profile["mo_list"])
    weapon = random.choice(profile["weapons"])
    gang_type = random.choice(profile["gang_types"])
    risk_level = random.choice(profile["risk_levels"])
    
    loc = random.choice(LOCATIONS)
    state = loc["state"]
    district = loc["district"]
    region = loc["region"]
    
    # Prior convictions correlate with age & risk
    if risk_level == "Critical":
        prior_convictions = random.randint(3, 11)
        active_warrants = random.randint(1, 4)
    elif risk_level == "High":
        prior_convictions = random.randint(1, 6)
        active_warrants = random.choice([0, 1, 2])
    elif risk_level == "Medium":
        prior_convictions = random.randint(0, 3)
        active_warrants = random.choice([0, 1])
    else:
        prior_convictions = random.choice([0, 1])
        active_warrants = 0
        
    height_cm = random.randint(156, 186)
    build = random.choice(BUILDS)
    complexion = random.choice(COMPLEXIONS)
    marks = random.choice(IDENTIFYING_MARKS)
    
    record_id = f"CR_IND_{idx:04d}"
    
    return {
        "record_id": record_id,
        "name": full_name,
        "alias": alias,
        "gender": gender,
        "age": age,
        "primary_crime_type": crime_type,
        "applicable_laws": applied_sections,
        "modus_operandi": mo,
        "weapon_used": weapon,
        "gang_affiliation": gang_type,
        "state": state,
        "district": district,
        "region": region,
        "prior_convictions": prior_convictions,
        "active_warrants": active_warrants,
        "height_cm": height_cm,
        "build": build,
        "complexion": complexion,
        "identifying_marks": marks,
        "risk_level": risk_level
    }

def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    csv_file = os.path.join(raw_dir, "criminal_records_dataset.csv")
    jsonl_file = os.path.join(processed_dir, "criminal_profiles_master.jsonl")
    
    records = [generate_record(i + 1) for i in range(NUM_RECORDS)]
    
    # 1. Export Tabular CSV for Offline ML Training (KNN / Random Forest / SVM)
    logger.info(f"Writing {NUM_RECORDS} tabular records to {csv_file}...")
    fieldnames = list(records[0].keys())
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    # 2. Export Unified JSONL Schema for RAG / Agent Retrieval Subsystem
    # Unified Schema: doc_id, content, doc_type, metadata
    logger.info(f"Writing unified JSONL records to {jsonl_file}...")
    with open(jsonl_file, "w", encoding="utf-8") as f:
        for r in records:
            content_desc = (
                f"Criminal Profile: {r['name']} (Alias: {r['alias']}). "
                f"Crime Type: {r['primary_crime_type']}. "
                f"Modus Operandi: {r['modus_operandi']}. "
                f"Applicable Laws: {r['applicable_laws']}. "
                f"Weapon: {r['weapon_used']}. "
                f"Area: {r['district']}, {r['state']} ({r['region']}). "
                f"Gang: {r['gang_affiliation']}. "
                f"Physical Traits: {r['height_cm']}cm, {r['build']} build, {r['complexion']} complexion. "
                f"Identifying Marks: {r['identifying_marks']}. "
                f"Prior Convictions: {r['prior_convictions']}, Active Warrants: {r['active_warrants']}, Risk: {r['risk_level']}."
            )
            
            unified_record = {
                "doc_id": r["record_id"].lower(),
                "content": content_desc,
                "doc_type": "criminal_profile",
                "metadata": {
                    "record_id": r["record_id"],
                    "name": r["name"],
                    "alias": r["alias"],
                    "age": r["age"],
                    "gender": r["gender"],
                    "primary_crime_type": r["primary_crime_type"],
                    "applicable_laws": r["applicable_laws"],
                    "modus_operandi": r["modus_operandi"],
                    "weapon_used": r["weapon_used"],
                    "gang_affiliation": r["gang_affiliation"],
                    "state": r["state"],
                    "district": r["district"],
                    "region": r["region"],
                    "prior_convictions": r["prior_convictions"],
                    "active_warrants": r["active_warrants"],
                    "risk_level": r["risk_level"],
                    "height_cm": r["height_cm"],
                    "build": r["build"],
                    "identifying_marks": r["identifying_marks"]
                }
            }
            f.write(json.dumps(unified_record, ensure_ascii=False) + "\n")
            
    logger.info(f"Successfully created Criminal Records Dataset with {NUM_RECORDS} individuals!")
    print(f"Generated {NUM_RECORDS} records in CSV and JSONL formats.")

if __name__ == "__main__":
    main()
