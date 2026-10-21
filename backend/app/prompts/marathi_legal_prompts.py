"""
NyayaAI Marathi Legal Prompt Templates for Maharashtra State & District Courts.
Formal governmental and judicial Marathi (प्रमाण न्यायालयीन मराठी भाषा).
Adheres strictly to the filing protocols and conventions of Maharashtra District & Sessions Courts,
Chief Judicial Magistrate (CJM), and Judicial Magistrate First Class (JMFC) Courts.
"""

# =====================================================================
# Official Judicial Marathi Terminology & Legal Lexicon (प्रमाण न्यायालयीन परिभाषा)
# =====================================================================
MARATHI_LEGAL_LEXICON = {
    # Judicial Authorities & Courts
    "High Court": "मा. उच्च न्यायालय",
    "Sessions Court": "मे. सत्र न्यायालय",
    "District & Sessions Court": "मे. जिल्हा व सत्र न्यायालय",
    "Judicial Magistrate First Class (JMFC)": "मे. प्रथम वर्ग न्यायदंडाधिकारी",
    "Chief Judicial Magistrate (CJM)": "मे. मुख्य न्यायदंडाधिकारी",
    
    # Parties & Role
    "Applicant / Accused": "अर्जदार / आरोपी",
    "Complainant / Informant": "फिर्यादी / तक्रारदार / खबर देणारा",
    "State of Maharashtra / Prosecution": "महाराष्ट्र शासन (मार्फत पोलीस ठाणे) / सामाईक",
    "Investigation Officer": "तपासिक अंमलदार / तपास अधिकारी",
    "Surety": "सक्षम व पतवान जमीनदार (Solvent Surety)",
    
    # Proceedings & Documents
    "First Information Report (FIR)": "प्रथम खबर अहवाल (गुन्हा नोंद क्र. / गु.र.नं.)",
    "Charge Sheet": "अंतिम दोषारोपपत्र (कलम १९३ BNSS / १७३ CrPC)",
    "Bail Application": "नियमित जामीन अर्ज (कलम ४८३ BNSS / ४३९ CrPC)",
    "Anticipatory Bail Application": "अटकपूर्व जामीन अर्ज (कलम ४८२ BNSS / ४३८ CrPC)",
    "Private Criminal Complaint": "खाजगी फौजदारी तक्रार (कलम २२३ BNSS / २०० CrPC)",
    "Discharge Application": "दोषमुक्तीचा अर्ज (कलम २५० BNSS / २२७, २३९ CrPC)",
    "Affidavit": "न्यायालयीन सत्यप्रतिज्ञा / प्रतिज्ञापत्र",
    "Written Arguments / Submissions": "लेखी युक्तिवाद / कैफियत",
    "Exemption Application": "आरोपीच्या व्यक्तिगत हजेरीतून सूट मिळणेबाबत अर्ज",
    
    # Procedural & Evidentiary Terms
    "Prima Facie Case": "प्रथमदर्शनी पुरावा / प्रथमदर्शनी प्रकरण",
    "Custodial Interrogation": "पोलीस कोठडीतील चौकशी / शारीरिक कोठडी",
    "Judicial Custody": "न्यायालयीन कोठडी (मॅजिस्ट्रेट कस्टडी)",
    "Statutory Notice under Sec 35 BNSS / 41A CrPC": "वैधानिक हजेरी नोटीस (कलम ३५ BNSS / ४१-अ CrPC)",
    "Seizure / Panchnama": "जप्ती पंचनामा / हस्तगत करणे",
    "Recovery under Sec 23 BSA / 27 Evidence Act": "शोध व हस्तगत पुरावा (कलम २३ BSA / २७ पुरावा कायदा)",
    "No Criminal Antecedents": "कोणताही पूर्वगुन्हेगारी इतिहास नाही (स्वच्छ चारित्र्य)",
    "Flight Risk": "परागंदा अथवा परागंदा होण्याची शक्यता",
    "Tampering with Evidence": "पुराव्यांशी छेडछाड करणे",
    "Influencing Witnesses": "साक्षीदारांवर दबाव किंवा प्रभाव आणणे",
    "Personal Recognizance / Bond": "वैयक्तिक जातमुचलका",
    "Solvent Surety": "स्थानिक पतवान जमीनदार",
    
    # Penal Provisions & Offence Descriptions
    "Cheating & Dishonest Inducement (Sec 420 IPC / 318 BNS)": "फसवणूक आणि अप्रामाणिकपणे मालमत्ता देण्यास प्रवृत्त करणे",
    "Criminal Breach of Trust (Sec 406 IPC / 316 BNS)": "आपराधिक विश्वासघात",
    "Forgery (Sec 465, 468 IPC / 336, 338 BNS)": "बनावट दस्तऐवज तयार करणे व वापरणे",
    "Criminal Conspiracy (Sec 120B IPC / 61 BNS)": "गुन्हेगारी स्वरूपाचा कट रचणे",
    "Common Intention (Sec 34 IPC / 3(5) BNS)": "सामाईक उद्देश साध्य करण्यासाठी केलेले कृत्य",
    "Cyber Impersonation (Sec 66D IT Act)": "माहिती तंत्रज्ञान साधनांचा वापर करून तोतयागिरीद्वारे फसवणूक",
    "Assault / Hurt (Sec 323, 324 IPC / 115, 117 BNS)": "स्वैर दुखापत / घातक हत्याराने मारहाण",
    "Attempt to Murder (Sec 307 IPC / 109 BNS)": "खुनाचा प्रयत्न",
    "Bail is the Rule, Jail is Exception": "जामीन हा नियम आहे आणि तुरुंगवास हा अपवाद आहे (सर्वोच्च न्यायालय तत्त्व)"
}

# =====================================================================
# Master Judicial Marathi System Prompt for LLMs
# =====================================================================
MARATHI_DRAFTING_SYSTEM_PROMPT = """तुम्ही मुंबई उच्च न्यायालय (Bombay High Court) तसेच महाराष्ट्र राज्यातील जिल्हा व सत्र न्यायालये (District & Sessions Courts) आणि प्रथम वर्ग न्यायदंडाधिकारी (JMFC) न्यायालयांमध्ये प्रदीर्घ अनुभव असलेले एक अत्यंत निष्णात, विद्वान वरिष्ठ फौजदारी अधिवक्ता (Senior Criminal Advocate) आहात.

तुमचे ध्येय:
दिलेल्या केसच्या वस्तुस्थितीवरून (Case Facts), गुन्ह्याच्या कलमांवरून आणि कायदेशीर पूर्वोदाहरणांवरून (RAG Precedents) न्यायालयात प्रत्यक्ष दाखल करता येईल असा १००% अस्सल, प्रमाणित आणि परिपूर्ण न्यायालयीन मराठी मसुदा (Court-Ready Legal Pleading) तयार करणे.

★★★ अत्यंत महत्त्वाचे कायदेशीर नियम व मसुदा लेखन शिष्टाचार ★★★

१. अस्सल न्यायालयीन मराठी भाषा (Strict Formal Judicial Marathi):
- मसुदा पूर्णपणे महाराष्ट्र न्यायालयांच्या प्रमाणित व प्रतिष्ठित भाषेत असला पाहिजे.
- इंग्रजी शब्दांचे चुकीचे शब्दशः भाषांतर (literal machine translation) अजिबात करू नका. (उदा. "गुन्हा घडवला गेला" किंवा "पोलीस स्टेशनने केस घेतली" असे न लिहिता "गुन्हा नोंदवण्यात आला", "तपास यंत्रणेने एफ.आय.आर. दाखल केला" असे लिहा).
- कायद्यातील अधिकृत संज्ञा वापरा: उदा. फिर्यादी, अर्जदार, सामाईक, गु.र.नं., वैधानिक नोटीस, सबळ कायदेशीर कारणे, हस्तगत पंचनामा, नम्र प्रार्थना, सत्यप्रतिज्ञा.

२. मसुद्याची अनिवार्य अधिकृत रचना (Mandatory Structure):
   [भाग १] न्यायालयीन शीर्षक (Court Name & Jurisdiction) - मध्यभागी ठळक अक्षरात
   [भाग २] केस प्रकार व वर्ष (उदा. फौजदारी जामीन अर्ज क्र. ____ / २०२४)
   [भाग ३] पक्षकारांचे नाव व पत्ता (Cause Title):
          - अर्जदार / आरोपी (नाव, वय, व्यवसाय, पत्ता)
          - विरुद्ध
          - सामाईक (महाराष्ट्र शासन, मार्फत तपास अधिकारी, पोलीस ठाणे)
   [भाग ४] गुन्ह्याचा संदर्भ: पोलीस ठाणे, गुन्हा रजिस्टर नंबर (गु.र.नं.), लागू कलमे (भा.दं.वि. / बी.एन.एस. / आय.टी. ॲक्ट / बी.एन.एस.एस.)
   [भाग ५] अर्जाचा विषय (Subject Line): कायदेशीर तरतुदींसह नेमका विषय.
   [भाग ६] सविनय प्रस्तावना: "मेहरबान न्यायालयापुढे अर्जदार तर्फे अत्यंत आदराने व नम्रपणे खालीलप्रमाणे सविनय अर्ज सादर करण्यात येत आहे:-"
   [भाग ७] प्रकरणाची पार्श्वभूमी व थोडक्यात वस्तुस्थिती (Brief Facts): परिच्छेद क्र. १, २, ३... स्वरूपात. इंग्रजीतील वस्तुस्थिती अस्सल न्यायालयीन मराठीत भाषांतरित करून अर्जदाराचा बचाव स्पष्ट करा.
   [भाग ८] अर्जाची सबळ कायदेशीर कारणे (Substantive Legal Grounds): (अ), (ब), (क)... स्वरूपात. खालील कायदेशीर तत्त्वे व सर्वोच्च न्यायालयाचे निकाल अनिवार्यपणे समाविष्ट करा:
          • बी.एन.एस.एस. कलम ३५ / CrPC कलम ४१-अ चे उल्लंघन (अर्नेश कुमार विरुद्ध बिहार राज्य तत्त्व).
          • ७ वर्षांपेक्षा कमी शिक्षेचे गुन्हे आणि सत्येंद्र कुमार अंतिल विरुद्ध सी.बी.आय. (2022) 10 SCC 51 मधील तत्त्वे.
          • जामीन हा नियम, तुरुंग हा अपवाद (संजय चंद्रा विरुद्ध सी.बी.आय. 2012 1 SCC 40).
          • अर्जदाराकडून कोणतीही अतिरिक्त जप्ती किंवा रिकव्हरी बाकी नसणे.
          • अर्जदाराचा कोणताही पूर्वगुन्हेगारी इतिहास (No criminal antecedents) नसणे.
          • अर्जदार स्थानिक रहिवासी असल्याने परागंदा होण्याची (Flight Risk) शक्यता नसणे.
   [भाग ९] अर्जदाराची न्यायालयीन हमी (Undertaking): अटींचे पालन, नियमित हजेरी, साक्षीदारांवर दबाव न आणणे, सक्षम जमीनदार देण्याची तयारी.
   [भाग १०] नम्र प्रार्थना (Prayer Clause): नेमकी कायदेशीर मागणी.
   [भाग ११] सत्यप्रतिज्ञा / पडताळणी (Verification Affidavit): तारीख, ठिकाण, अर्जदार व वकिलांची स्वाक्षरी जागा.

३. शुद्धलेखन व टंकलेखन:
- आउटपुट स्वच्छ, सुवाच्य आणि कोर्टाच्या लीगल पेपरवर थेट प्रिंट करून दाखल करता येईल अशा उच्च दर्जाचे द्या.
"""

# =====================================================================
# Specialized Drafting Prompts for All Pleading Types
# =====================================================================
def get_marathi_draft_prompt(
    draft_type: str,
    court_name: str,
    applicant_name: str,
    opponent_name: str,
    police_station: str,
    fir_number: str,
    sections: str,
    facts: str,
    additional_grounds: str = "",
    rag_context: str = ""
) -> str:
    """
    Constructs a highly structured, court-ready prompt for generating specific
    criminal pleadings in formal judicial Marathi for Maharashtra Courts.
    """
    draft_type_titles = {
        "bail_application": "नियमित जामीन अर्ज (Regular Bail Application under Sec 483 BNSS, 2023 / Sec 437/439 CrPC)",
        "anticipatory_bail": "अटकपूर्व जामीन अर्ज (Anticipatory Bail Application under Sec 482 BNSS, 2023 / Sec 438 CrPC)",
        "criminal_complaint": "खाजगी फौजदारी तक्रार अर्ज (Private Criminal Complaint under Sec 223 BNSS / Sec 156(3) & 200 CrPC)",
        "discharge_application": "दोषमुक्तीचा अर्ज (Discharge Application under Sec 250 BNSS / Sec 227 & 239 CrPC)",
        "affidavit": "न्यायालयीन शपथपत्र / सत्यप्रतिज्ञा (Affidavit in Support of Application)",
        "exemption_application": "आरोपीच्या व्यक्तिगत हजेरीतून सूट मिळणेबाबत अर्ज (Exemption Application under Sec 228 BNSS / Sec 205 CrPC)",
        "written_arguments": "लेखी युक्तिवाद / कैफियत (Written Arguments & Submissions on behalf of Applicant)"
    }

    selected_title = draft_type_titles.get(draft_type, "फौजदारी न्यायालयीन अर्ज (Criminal Court Application)")

    specific_guidance = ""
    if draft_type == "anticipatory_bail":
        specific_guidance = """
विशेष सूचना (अटकपूर्व जामीन):
- अर्जदाराला पोलिसांकडून अटक होण्याची रास्त व सकारण भीती (Reasonable apprehension of arrest) का वाटते हे स्पष्ट करा.
- मा. सर्वोच्च न्यायालयाच्या 'गुर्बक्ष सिंग सिब्बिया विरुद्ध पंजाब राज्य (1980) 2 SCC 565' आणि 'सुशीला अग्रवाल विरुद्ध राज्य (NCT दिल्ली) (2020) 5 SCC 1' या निकालांचा संदर्भ द्या.
- प्रार्थना: "सदर गुन्ह्यात अर्जदारास अटक झाल्यास त्याची तात्काळ योग्य त्या जामिनावर मुक्तता करण्यात यावी."
"""
    elif draft_type == "criminal_complaint":
        specific_guidance = """
विशेष सूचना (खाजगी फौजदारी तक्रार):
- फिर्यादीची खरी बाजू, आरोपीने केलेली फसवणूक, कट आणि आर्थिक नुकसान यांचा घटनाक्रम तारीखनिहाय नमूद करा.
- पुराव्याची कागदपत्रे व साक्षीदारांची यादी (List of Witnesses) जोडा.
- प्रार्थना: आरोपीविरुद्ध कायद्यानुसार दखल घेऊन योग्य ती कायदेशीर कारवाई (Process Issue) करावी किंवा तपासाचे आदेश द्यावेत.
"""
    elif draft_type == "discharge_application":
        specific_guidance = """
विशेष सूचना (दोषमुक्तीचा अर्ज):
- पोलिसांनी दाखल केलेल्या दोषारोपपत्रात (Charge Sheet) अर्जदाराविरुद्ध कोणताही प्रथमदर्शनी पुरावा नसल्याचे सविस्तर दाखवा.
- केवळ संशयाच्या आधारे खटला चालवणे कायद्याच्या प्रक्रियेचा दुरुपयोग कसा आहे हे सिद्ध करा.
- प्रार्थना: अर्जदारास सदर गुन्ह्यातून ससन्मान दोषमुक्त (Discharged) करण्यात यावे.
"""

    rag_block = ""
    if rag_context:
        rag_block = f"""
### ४. आर.ए.जी. कायदेशीर पूर्वोदाहरण व वैधानिक कलमे (Retrieved RAG Precedents & Statutes):
{rag_context}
(टीप: वरील आर.ए.जी. निकालांचा आणि वैधानिक तरतुदींचा मसुद्याच्या 'सबळ कायदेशीर कारणे' विभागात प्रभावीपणे उपयोग करा.)
"""

    return f"""खालील माहितीचा काळजीपूर्वक अभ्यास करून महाराष्ट्र राज्यातील न्यायालयात दाखल करण्यासाठी '{selected_title}' चा १००% अस्सल, परिपूर्ण आणि कोर्ट-तयार (Court-Ready) न्यायालयीन मसुदा तयार करा:

### १. न्यायालयीन व केस संदर्भ (Court & Case Details):
- न्यायालय: {court_name if court_name else "मे. सत्र न्यायालय, पुणे"}
- अर्जदार / आरोपीचे नाव: {applicant_name if applicant_name else "अर्जदार"}
- सामाईक / फिर्यादी: {opponent_name if opponent_name else "महाराष्ट्र शासन (मार्फत पोलीस ठाणे)"}
- पोलीस ठाणे: {police_station if police_station else "स्थानिक पोलीस ठाणे"}
- गुन्हा नोंद (FIR) क्र. व वर्ष: {fir_number if fir_number else "गु.र.नं. लागू नाही"}
- लागू कलमे (Statutory Sections): {sections if sections else "भा.दं.वि. / बी.एन.एस. / बी.एन.एस.एस."}

### २. केसची वस्तुस्थिती (Factual Background & Defense Narrative):
{facts}

### ३. अर्जदाराचे बचावाचे मुद्दे / अतिरिक्त कारणे (Additional Defense Grounds):
{additional_grounds if additional_grounds else "अर्जदार कायद्याचे पालन करणारा प्रतिष्ठित नागरिक असून त्याला केवळ संशयावरून गोवण्यात आले आहे."}
{rag_block}
{specific_guidance}

### मसुद्याचा आवश्यक अधिकृत आराखडा (Strict Court Drafting Structure):
१. **न्यायालयीन शीर्षक**: मे. न्यायालयाचे नाव व शहर (ठळक व मध्यभागी).
२. **केस प्रकार व क्रमांक**: उदा. फौजदारी जामीन अर्ज क्र. ____ / २०२४.
३. **कारणनामा (Cause Title)**:
   - अर्जदाराचे संपूर्ण नाव, वय, पत्ता ... अर्जदार / आरोपी
   - विरुद्ध
   - महाराष्ट्र शासन, मार्फत तपास अधिकारी ... सामाईक / सरकार
४. **गुन्हा संदर्भ**: पोलीस ठाणे, गु.र.नं., लागू कलमे.
५. **अर्जाचा विषय**: कायद्याच्या योग्य कलमांचा उल्लेख करून नेमका विषय.
६. **प्रस्तावना**: "मेहरबान न्यायालयापुढे अर्जदारतर्फे अत्यंत आदराने व नम्रपणे खालीलप्रमाणे सविनय अर्ज सादर करण्यात येत आहे:-"
७. **केसची सविस्तर वस्तुस्थिती**: परिच्छेद क्र. १, २, ३... मध्ये (इंग्रजीतील केस फॅक्ट्स अस्सल न्यायालयीन मराठीत रूपांतरित करा).
८. **अर्जाची सबळ कायदेशीर कारणे**: (अ), (ब), (क)... मध्ये कायदेशीर तत्त्वांसह व आर.ए.जी. निकालांसह.
९. **अर्जदाराची न्यायालयीन हमी व तत्परता**: अटींचे पालन व सक्षम जमीनदार देण्याची तयारी.
१०. **नम्र प्रार्थना (Prayer Clause)**: नेमका कायदेशीर दिलासा मिळणेबाबत.
११. **सत्यप्रतिज्ञा (Verification Affidavit)**: तारीख, ठिकाण, अर्जदार स्वाक्षरी व अधिवक्ता स्वाक्षरी.

हा मसुदा पूर्णपणे अस्सल, व्याकरणदृष्ट्या निर्दोष आणि उच्च दर्जाच्या प्रमाण न्यायालयीन मराठी भाषेत (Formal Judicial Marathi) लिहा.
"""
