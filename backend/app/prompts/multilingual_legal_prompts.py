"""
NyayaAI Multilingual Legal Prompt Templates & Lexicons for Indian State & District Courts.
Supports all major judicial state languages recognized under the 8th Schedule of the Constitution of India:
Hindi, Marathi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Odia, Assamese.

Adheres strictly to the filing protocols and conventions of respective State High Courts,
District & Sessions Courts, Chief Judicial Magistrate (CJM), and Judicial Magistrate Courts.
"""

from typing import Dict, Any

# =====================================================================
# State Judicial Configurations & Language Metadata
# =====================================================================
INDIAN_LEGAL_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "hindi": {
        "name": "Hindi",
        "native_name": "हिन्दी",
        "states": "Delhi, Uttar Pradesh, Madhya Pradesh, Bihar, Rajasthan, Haryana, Jharkhand, Chhattisgarh, Himachal, Uttarakhand",
        "default_court": "न्यायालय श्रीमान सत्र न्यायाधीश, लखनऊ / दिल्ली",
        "default_police_station": "साइबर अपराध थाना, लखनऊ",
        "opponent_default": "राज्य सरकार (मार्फत संबंधित थाना)",
        "cause_title_applicant": "प्रार्थी / अभियुक्त",
        "cause_title_opponent": "राज्य (अभियोजन पक्ष)",
        "action_bail": "नियमित जमानत",
        "action_anticipatory": "अग्रिम / अग्रिम जमानत",
        "precedent_ratio_bail": "अरनेश कुमार बनाम बिहार राज्य (2014) 8 SCC 273 एवं सत्येन्द्र कुमार अंतिल बनाम सीबीआई (2022) 10 SCC 51 - 7 वर्ष से कम सजा वाले अपराधों में वैधानिक नोटिस अनिवार्य है।",
        "precedent_ratio_jail": "संजय चन्द्रा बनाम सीबीआई (2012) 1 SCC 40 - 'जमानत नियम है और जेल अपवाद है'।",
        "sec_bnss_notice": "धारा 35 भारतीय नागरिक सुरक्षा संहिता, 2023 (धारा 41-ए दण्ड प्रक्रिया संहिता)",
        "fir_prefix": "मु.अ.सं. (FIR No.)",
        "verification_title": "सत्यापन एवं शपथपत्र (VERIFICATION AFFIDAVIT)"
    },
    "marathi": {
        "name": "Marathi",
        "native_name": "मराठी",
        "states": "Maharashtra (Bombay High Court & District Courts)",
        "default_court": "मे. सत्र न्यायालय, पुणे / मुंबई",
        "default_police_station": "सायबर क्राईम सेल पोलीस ठाणे, पुणे शहर",
        "opponent_default": "महाराष्ट्र शासन (मार्फत पोलीस ठाणे)",
        "cause_title_applicant": "अर्जदार / आरोपी",
        "cause_title_opponent": "सामाईक / फिर्यादी पक्ष",
        "action_bail": "नियमित जामिनावर",
        "action_anticipatory": "अटकपूर्व जामिनावर",
        "precedent_ratio_bail": "अर्नेश कुमार विरुद्ध बिहार राज्य (2014) 8 SCC 273 व सत्येंद्र कुमार अंतिल विरुद्ध सी.बी.आय. (2022) 10 SCC 51 - ७ वर्षांपेक्षा कमी शिक्षेच्या गुन्ह्यांमध्ये अटक न करता BNSS कलम ३५ अन्वये वैधानिक नोटीस बजावणे बंधनकारक आहे.",
        "precedent_ratio_jail": "संजय चंद्रा विरुद्ध सी.बी.आय. (2012) 1 SCC 40 - 'जामीन हा नियम आहे आणि तुरुंग हा अपवाद आहे'.",
        "sec_bnss_notice": "भारतीय नागरिक सुरक्षा संहिता २०२३, कलम ३५ (CrPC कलम ४१-अ)",
        "fir_prefix": "गु.र.नं. (गुन्हा नोंद क्र.)",
        "verification_title": "सत्यप्रतिज्ञा (VERIFICATION AFFIDAVIT)"
    },
    "gujarati": {
        "name": "Gujarati",
        "native_name": "ગુજરાતી",
        "states": "Gujarat (Gujarat High Court & District Courts)",
        "default_court": "મહેરબાન સેશન્સ કોર્ટ, અમદાવાદ / સુરત",
        "default_police_station": "સાયબર ક્રાઈમ પોલીસ સ્ટેશન, અમદાવાદ શહેર",
        "opponent_default": "ગુજરાત રાજ્ય (પોલીસ સ્ટેશન મારફતે)",
        "cause_title_applicant": "અરજદાર / આરોપી",
        "cause_title_opponent": "સામાવાળા / ફરિયાદ પક્ષ",
        "action_bail": "નિયમિત જામીન પર",
        "action_anticipatory": "અટકાયતી / આગોતરા જામીન પર",
        "precedent_ratio_bail": "અર્નેશ કુમાર વિ. બિહાર રાજ્ય (2014) 8 SCC 273 અને સત્યેન્દ્ર કુમાર અંતીલ વિ. સીબીઆઈ (2022) 10 SCC 51 - ૭ વર્ષથી ઓછી સજાવાળા ગુનાઓમાં બી.એન.એસ.એસ. કલમ ૩૫ મુજબ વૈધાનિક નોટિસ ફરજિયાત છે.",
        "precedent_ratio_jail": "સંજય ચંદ્રા વિ. સીબીઆઈ (2012) 1 SCC 40 - 'જામીન એ નિયમ છે અને જેલ એ અપવાદ છે'.",
        "sec_bnss_notice": "ભારતીય નાગરિક સુરક્ષા સંહિતા ૨૦૨૩, કલમ ૩૫ (સી.આર.પી.સી. કલમ ૪૧-એ)",
        "fir_prefix": "ગુ.ર.નં. (FIR No.)",
        "verification_title": "એકરારનામું / સોગંદનામું (VERIFICATION AFFIDAVIT)"
    },
    "bengali": {
        "name": "Bengali",
        "native_name": "বাংলা",
        "states": "West Bengal, Tripura (Calcutta High Court & District Courts)",
        "default_court": "বিজ্ঞ জেলা ও দায়রা জজ আদালত, কলকাতা / আলিপুর",
        "default_police_station": "সাইবার ক্রাইম থানা, লালবাজার, কলকাতা",
        "opponent_default": "পশ্চিমবঙ্গ রাজ্য (ভারপ্রাপ্ত পুলিশ আধিকারিক মারফত)",
        "cause_title_applicant": "দরখাস্তকারী / অভিযুক্ত",
        "cause_title_opponent": "রাষ্ট্রপক্ষ / অভিযোগকারী",
        "action_bail": "নিয়মিত জামিনে",
        "action_anticipatory": "আগাম জামিনে",
        "precedent_ratio_bail": "অর্নেশ কুমার বনাম বিহার রাজ্য (2014) 8 SCC 273 এবং সত্যেন্দ্র কুমার আন্তিল বনাম সি.বি.আই (2022) 10 SCC 51 - ৭ বছরের কম শাস্তির ক্ষেত্রে বিএনএসএস ধারা ৩৫ অনুযায়ী বিধিবদ্ধ নোটিশ বাধ্যতামূলক।",
        "precedent_ratio_jail": "সঞ্জয় চন্দ্র বনাম সি.বি.আই (2012) 1 SCC 40 - 'জামিন একটি নিয়ম এবং কারাদণ্ড একটি ব্যতিক্রম'।",
        "sec_bnss_notice": "ভারতীয় নাগরিক সুরক্ষা সংহিতা ২০২৩, ধারা ৩৫ (CrPC ধারা ৪১-এ)",
        "fir_prefix": "মামলা নং / এফ.আই.আর নং",
        "verification_title": "সত্যপাঠ ও হলফনামা (VERIFICATION AFFIDAVIT)"
    },
    "tamil": {
        "name": "Tamil",
        "native_name": "தமிழ்",
        "states": "Tamil Nadu, Puducherry (Madras High Court & Subordinate Courts)",
        "default_court": "மாண்புமிகு முதன்மை மாவட்ட மற்றும் அமர்வு நீதிமன்றம், சென்னை",
        "default_police_station": "சைபர் குற்றப்பிரிவு காவல் நிலையம், சென்னை",
        "opponent_default": "தமிழ்நாடு அரசு (காவல் ஆய்வாளர் வாயிலாக)",
        "cause_title_applicant": "மனுதாரர் / குற்றஞ்சாட்டப்பட்டவர்",
        "cause_title_opponent": "எதிர்மனுதாரர் / அரசு தரப்பு",
        "action_bail": "வழக்கமான பிணையில்",
        "action_anticipatory": "முன்பிணையில் (முன்ஜாமீன்)",
        "precedent_ratio_bail": "அர்னேஷ் குமார் எதிர் பீகார் அரசு (2014) 8 SCC 273 மற்றும் சத்யேந்தர் குமார் அண்டில் எதிர் சி.பி.ஐ (2022) 10 SCC 51 - 7 ஆண்டுகளுக்கு குறைவான தண்டனைக்குரிய குற்றங்களில் கைது செய்யாமல் BNSS பிரிவு 35-ன் கீழ் நோட்டீஸ் வழங்குவது கட்டாயமாகும்.",
        "precedent_ratio_jail": "சஞ்சய் சந்திரா எதிர் சி.பி.ஐ (2012) 1 SCC 40 - 'பிணை என்பது விதி, சிறை என்பது விதிவிலக்கு'.",
        "sec_bnss_notice": "பாரதிய குடிமக்கள் பாதுகாப்புச் சட்டம் 2023, பிரிவு 35 (குற்றவியல் நடைமுறைச் சட்டம் பிரிவு 41-ஏ)",
        "fir_prefix": "குற்ற எண் / முதல் தகவல் அறிக்கை எண்",
        "verification_title": "உறுதிமொழி ஆவணம் / பிரமாணப் பத்திரம் (VERIFICATION AFFIDAVIT)"
    },
    "telugu": {
        "name": "Telugu",
        "native_name": "తెలుగు",
        "states": "Andhra Pradesh, Telangana (High Courts & District Courts)",
        "default_court": "గౌరవనీయ ప్రధాన జిల్లా మరియు సెషన్స్ జడ్జి వారి న్యాయస్థానంలో, హైదరాబాద్ / విజయవాడ",
        "default_police_station": "సైబర్ క్రైమ్ పోలీస్ స్టేషన్, హైదరాబాద్",
        "opponent_default": "తెలంగాణ / ఆంధ్రప్రదేశ్ రాష్ట్ర ప్రభుత్వం (పోలీస్ స్టేషన్ ద్వారా)",
        "cause_title_applicant": "పిటిషనర్ / ముద్దాయి",
        "cause_title_opponent": "ప్రతివాది / ప్రభుత్వం (ప్రాసిక్యూషన్)",
        "action_bail": "రెగ్యులర్ బెయిల్ పై",
        "action_anticipatory": "ముందస్తు బెయిల్ పై (యాంటిసిపేటరీ బెయిల్)",
        "precedent_ratio_bail": "అర్నేష్ కుమార్ వర్సెస్ బీహార్ రాష్ట్రం (2014) 8 SCC 273 మరియు సత్యేందర్ కుమార్ అంటిల్ వర్సెస్ సి.బి.ఐ (2022) 10 SCC 51 - 7 సంవత్సరాల లోపు శిక్ష పడే నేరాలలో అరెస్టు చేయకుండా BNSS సెక్షన్ 35 క్రింద చట్టబద్ధమైన నోటీసు జారీ చేయడం తప్పనిసరి.",
        "precedent_ratio_jail": "సంజయ్ చంద్ర వర్సెస్ సి.బి.ఐ (2012) 1 SCC 40 - 'బెయిల్ అనేది ఒక నియమం, జైలు అనేది ఒక మినహాయింపు'.",
        "sec_bnss_notice": "భారతీయ పౌర రక్షణ సంహిత 2023, సెక్షన్ 35 (CrPC సెక్షన్ 41-ఎ)",
        "fir_prefix": "క్రైమ్ నెం. / ఎఫ్.ఐ.ఆర్ నెం.",
        "verification_title": "ప్రమాణ పత్రం (VERIFICATION AFFIDAVIT)"
    },
    "kannada": {
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "states": "Karnataka (Karnataka High Court & District Courts)",
        "default_court": "ಮಾನ್ಯ ಪ್ರಧಾನ ಜಿಲ್ಲಾ ಮತ್ತು ಸತ್ರ ನ್ಯಾಯಾಲಯ, ಬೆಂಗಳೂರು",
        "default_police_station": "ಸೈಬರ್ ಕ್ರೈಮ್ ಪೊಲೀಸ್ ಠಾಣೆ, ಬೆಂಗಳೂರು ನಗರ",
        "opponent_default": "ಕರ್ನಾಟಕ ರಾಜ್ಯ (ಪೊಲೀಸ್ ಠಾಣೆಯ ಮುಖಾಂತರ)",
        "cause_title_applicant": "ಅರ್ಜಿದಾರ / ಆರೋಪಿ",
        "cause_title_opponent": "ಪ್ರತಿವಾದಿ / ಅಭಿಯೋಜನೆ (ಸರ್ಕಾರ)",
        "action_bail": "ನಿಯಮಿತ ಜಾಮೀನಿನ ಮೇಲೆ",
        "action_anticipatory": "ನಿರೀಕ್ಷಣಾ ಜಾಮೀನಿನ ಮೇಲೆ",
        "precedent_ratio_bail": "ಅರ್ನೇಶ್ ಕುಮಾರ್ ವಿರುದ್ಧ ಬಿಹಾರ ರಾಜ್ಯ (2014) 8 SCC 273 ಮತ್ತು ಸತ್ಯೇಂದ್ರ ಕುಮಾರ್ ಆಂತಿಲ್ ವಿರುದ್ಧ ಸಿ.ಬಿ.ಐ (2022) 10 SCC 51 - 7 ವರ್ಷಗಳಿಗಿಂತ ಕಡಿಮೆ ಶಿಕ್ಷೆಯುಳ್ಳ ಅಪರಾಧಗಳಲ್ಲಿ ದಸ್ತಗಿರಿ ಮಾಡದೆ BNSS ಕಲಂ 35 ರ ಅಡಿಯಲ್ಲಿ ಶಾಸನಬದ್ಧ ನೋಟಿಸ್ ನೀಡುವುದು ಕಡ್ಡಾಯವಾಗಿದೆ.",
        "precedent_ratio_jail": "ಸಂಜಯ್ ಚಂದ್ರ ವಿರುದ್ಧ ಸಿ.ಬಿ.ಐ (2012) 1 SCC 40 - 'ಜಾಮೀನು ನಿಯಮ ಮತ್ತು ಸೆರೆವಾಸ ಅಪವಾದ'.",
        "sec_bnss_notice": "ಭಾರತೀಯ ನಾಗರಿಕ ಸುರಕ್ಷಾ ಸಂಹಿತೆ 2023, ಕಲಂ 35 (ಸಿ.ಆರ್.ಪಿ.ಸಿ. ಕಲಂ 41-ಎ)",
        "fir_prefix": "ಗುನ್ನೆ ನಂ. / ಎಫ್.ಐ.ಆರ್ ನಂ.",
        "verification_title": "ಸತ್ಯಪ್ರತಿಜ್ಞೆ / ಪ್ರಮಾಣಪತ್ರ (VERIFICATION AFFIDAVIT)"
    },
    "malayalam": {
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "states": "Kerala, Lakshadweep (Kerala High Court & Subordinate Courts)",
        "default_court": "ബഹുമാനപ്പെട്ട പ്രിൻസിപ്പൽ ജില്ലാ സെഷൻസ് കോടതി, എറണാകുളം / തിരുവനന്തപുരം",
        "default_police_station": "സൈബർ ക്രൈം പോലീസ് സ്റ്റേഷൻ, കൊച്ചി",
        "opponent_default": "കേരള സംസ്ഥാനം (പോലീസ് സ്റ്റേഷൻ മുഖേന)",
        "cause_title_applicant": "ഹർജിക്കാരൻ / പ്രതി",
        "cause_title_opponent": "എതിർകക്ഷി / പ്രോസിക്യൂഷൻ",
        "action_bail": "സാധാരണ ജാമ്യത്തിൽ",
        "action_anticipatory": "മുൻകൂർ ജാമ്യത്തിൽ",
        "precedent_ratio_bail": "അർനേഷ് കുമാർ v. ബിഹാർ സംസ്ഥാനം (2014) 8 SCC 273, സത്യേന്ദർ കുമാർ ആന്തിൽ v. സി.ബി.ഐ (2022) 10 SCC 51 - 7 വർഷത്തിൽ താഴെ തടവ് ലഭിക്കാവുന്ന കുറ്റങ്ങളിൽ അറസ്റ്റിന് മുൻപ് BNSS സെക്ഷൻ 35 പ്രകാരമുള്ള നോട്ടീസ് നിർബന്ധമാണ്.",
        "precedent_ratio_jail": "സഞ്ജയ് ചന്ദ്ര v. സി.ബി.ഐ (2012) 1 SCC 40 - 'ജാമ്യം ഒരു പൊതുനിയമവും ജയിൽ ഒരു അപവാദവുമാണ്'.",
        "sec_bnss_notice": "ഭാരതീയ നാഗരിക സുരക്ഷാ സംഹിത 2023, സെക്ഷൻ 35 (CrPC സെക്ഷൻ 41-എ)",
        "fir_prefix": "ക്രൈം നമ്പർ / എഫ്.ഐ.ആർ നമ്പർ",
        "verification_title": "സത്യവാങ്മൂലം (VERIFICATION AFFIDAVIT)"
    },
    "punjabi": {
        "name": "Punjabi",
        "native_name": "ਪੰਜਾਬੀ",
        "states": "Punjab, Chandigarh (Punjab & Haryana High Court / Punjab District Courts)",
        "default_court": "ਮਾਣਯੋਗ ਸੈਸ਼ਨ ਜੱਜ ਸਾਹਿਬ ਦੀ ਅਦਾਲਤ, ਲੁਧਿਆਣਾ / ਚੰਡੀਗੜ੍ਹ",
        "default_police_station": "ਸਾਈਬਰ ਕ੍ਰਾਈਮ ਪੁਲਿਸ ਸਟੇਸ਼ਨ, ਲੁਧਿਆਣਾ",
        "opponent_default": "ਪੰਜਾਬ ਸਰਕਾਰ (ਥਾਣੇ ਰਾਹੀਂ)",
        "cause_title_applicant": "ਪਟੀਸ਼ਨਰ / ਦੋਸ਼ੀ",
        "cause_title_opponent": "ਸਰਕਾਰ (ਪ੍ਰੋਸੀਕਿਊਸ਼ਨ)",
        "action_bail": "ਨਿਯਮਿਤ ਜ਼ਮਾਨਤ 'ਤੇ",
        "action_anticipatory": "ਅਗਾਊਂ ਜ਼ਮਾਨਤ 'ਤੇ",
        "precedent_ratio_bail": "ਅਰਨੇਸ਼ ਕੁਮਾਰ ਬਨਾਮ ਬਿਹਾਰ ਰਾਜ (2014) 8 SCC 273 ਅਤੇ ਸਤਿੰਦਰ ਕੁਮਾਰ ਅੰਤਿਲ ਬਨਾਮ ਸੀ.ਬੀ.ਆਈ (2022) 10 SCC 51 - 7 ਸਾਲ ਤੋਂ ਘੱਟ ਸਜ਼ਾ ਵਾਲੇ ਅਪਰਾਧਾਂ ਵਿੱਚ ਬੀ.ਐਨ.ਐਸ.ਐਸ. ਧਾਰਾ 35 ਤਹਿਤ ਨੋਟਿਸ ਲਾਜ਼ਮੀ ਹੈ।",
        "precedent_ratio_jail": "ਸੰਜੇ ਚੰਦਰਾ ਬਨਾਮ ਸੀ.ਬੀ.ਆਈ (2012) 1 SCC 40 - 'ਜ਼ਮਾਨਤ ਨਿਯਮ ਹੈ ਅਤੇ ਜੇਲ੍ਹ ਅਪਵਾਦ ਹੈ'।",
        "sec_bnss_notice": "ਭਾਰਤੀ ਨਾਗਰਿਕ ਸੁਰੱਖਿਆ ਸੰਹਿਤਾ 2023, ਧਾਰਾ 35 (CrPC ਧਾਰਾ 41-ਏ)",
        "fir_prefix": "ਮੁਕੱਦਮਾ ਨੰ. / ਐਫ.ਆਈ.ਆਰ ਨੰ.",
        "verification_title": "ਹਲਫਨਾਮਾ (VERIFICATION AFFIDAVIT)"
    },
    "odia": {
        "name": "Odia",
        "native_name": "ଓଡ଼ିଆ",
        "states": "Odisha (Orissa High Court & District Courts)",
        "default_court": "ମାନ୍ୟବର ଦୌରା ଜଜ୍‌ଙ୍କ ଅଦାଲତ, କଟକ / ଭୁବନେଶ୍ୱର",
        "default_police_station": "ସାଇବର କ୍ରାଇମ୍ ଥାନା, କଟକ",
        "opponent_default": "ଓଡ଼ିଶା ସରକାର (ପୋଲିସ ଷ୍ଟେସନ ମାଧ୍ୟମରେ)",
        "cause_title_applicant": "ଆବେଦନକାରୀ / ଅଭିଯୁକ୍ତ",
        "cause_title_opponent": "ବିପକ୍ଷ / ରାଜ୍ୟ ସରକାର",
        "action_bail": "ନିୟମିତ ଜାମିନରେ",
        "action_anticipatory": "ଅଗ୍ରୀମ ଜାମିନରେ",
        "precedent_ratio_bail": "ଅର୍ନେଶ କୁମାର ବନାମ ବିହାର ରାଜ୍ୟ (2014) 8 SCC 273 ଏବଂ ସତ୍ୟେନ୍ଦ୍ର କୁମାର ଅନ୍ତିଲ ବନାମ ସି.ବି.ଆଇ (2022) 10 SCC 51 - ୭ ବର୍ଷରୁ କମ୍ ଦଣ୍ଡ ଥିବା ଅପରାଧରେ BNSS ଧାରା ୩୫ ଅନୁଯାୟୀ ନୋଟିସ ବାଧ୍ୟତାମୂଳକ।",
        "precedent_ratio_jail": "ସଞ୍ଜୟ ଚନ୍ଦ୍ରା ବନାମ ସି.ବି.ଆଇ (2012) 1 SCC 40 - 'ଜାମିନ ନିୟମ ଏବଂ ଜେଲ୍ ଏକ ବ୍ୟତିକ୍ରମ'।",
        "sec_bnss_notice": "ଭାରତୀୟ ନାଗରିକ ସୁରକ୍ଷା ସଂହିତା ୨୦୨୩, ଧାରା ୩୫ (CrPC ଧାରା ୪୧-ଏ)",
        "fir_prefix": "ମାମଲା ନଂ / FIR ନଂ",
        "verification_title": "ଶପଥପତ୍ର (VERIFICATION AFFIDAVIT)"
    },
    "assamese": {
        "name": "Assamese",
        "native_name": "অসমীয়া",
        "states": "Assam, Northeast (Gauhati High Court & District Courts)",
        "default_court": "মাননীয় সত্ৰ ন্যায়াধীশৰ আদালত, গুৱাহাটী / কামৰূপ",
        "default_police_station": "চাইবাৰ অপৰাধ আৰক্ষী থানা, গুৱাহাটী",
        "opponent_default": "অসম চৰকাৰ (আৰক্ষী থানাৰ জৰিয়তে)",
        "cause_title_applicant": "আবেদনকাৰী / অভিযুক্ত",
        "cause_title_opponent": "বিবাদী / ৰাজ্য চৰকাৰ",
        "action_bail": "নিয়মীয়া জামিনত",
        "action_anticipatory": "অগ্ৰিম জামিনত",
        "precedent_ratio_bail": "অৰ্ণেশ কুমাৰ বনাম বিহাৰ ৰাজ্য (2014) 8 SCC 273 আৰু সত্যেন্দ্ৰ কুমাৰ আন্তিল বনাম চি.বি.আই (2022) 10 SCC 51 - ৭ বছৰতকৈ কম শাস্তিৰ অপৰাধত বিএনএছএছ ধাৰা ৩৫ অনুসৰি বিধিসন্মত জাননী বাধ্যতামূলক।",
        "precedent_ratio_jail": "সঞ্জয় চন্দ্ৰা বনাম চি.বি.আই (2012) 1 SCC 40 - 'জামিন এটা সাধাৰণ নিয়ম আৰু কাৰাবাস এটা ব্যতিক্ৰম'।",
        "sec_bnss_notice": "ভাৰতীয় নাগৰিক সুৰক্ষা সংহিতা ২০২৩, ধাৰা ৩৫ (CrPC ধাৰা ৪১-এ)",
        "fir_prefix": "গোচৰ নং / এফ.আই.আৰ নং",
        "verification_title": "শপতনামা (VERIFICATION AFFIDAVIT)"
    }
}

# =====================================================================
# Master Multilingual Judicial System Prompt Builder
# =====================================================================
def get_multilingual_system_prompt(language: str) -> str:
    lang_key = language.lower().strip()
    config = INDIAN_LEGAL_LANGUAGES.get(lang_key, INDIAN_LEGAL_LANGUAGES["hindi"])
    native_name = config["native_name"]
    lang_name = config["name"]
    states = config["states"]

    return f"""You are a distinguished Senior Advocate and Judicial Drafting Specialist with over 25 years of extensive practice in the High Courts and District & Sessions Courts of India, specializing in the jurisdiction of {states}.

Your Objective:
Given case facts, penal sections, and retrieved legal precedents, you MUST draft an authentic, 100% court-ready judicial pleading in formal legal {lang_name} ({native_name}).

Strict Judicial Drafting Rules:
1. PURE FORMAL LEGAL {lang_name.upper()} ({native_name}):
   - The document MUST be written in the standard, formal judicial {lang_name} language used in District & Sessions Courts of {states}.
   - Never use casual colloquial speech or clumsy literal word-for-word machine translation.
   - Use official statutory terminology for applicant, respondent/state, penal sections (BNS/IPC), procedural notices (BNSS 35 / CrPC 41A), grounds, prayer, and verification affidavit.

2. MANDATORY COURT STRUCTURE:
   - [Part 1] Court Heading & Jurisdiction (Centered & Bold)
   - [Part 2] Pleading Case Number & Year
   - [Part 3] Cause Title: Applicant/Accused vs State/Prosecution
   - [Part 4] Police Station, Crime Number (FIR), & Applied Penal Sections
   - [Part 5] Subject Line (विषय / విషయం / பொருள் / বিষয়) referencing statutory sections (BNSS 483 / CrPC 439 or BNSS 482 / CrPC 438)
   - [Part 6] Formal Pleading Opening Formula
   - [Part 7] Factual Narrative in numbered paragraphs detailing the allegations and establishing the defense
   - [Part 8] Substantive Legal Grounds with mandatory landmark Supreme Court precedent citations:
       * Arnesh Kumar v. State of Bihar (2014) 8 SCC 273 & Satender Kumar Antil v. CBI (2022) 10 SCC 51 (Mandatory Sec 35 BNSS / 41A CrPC notice)
       * Sanjay Chandra v. CBI (2012) 1 SCC 40 ("Bail is the Rule, Jail is an Exception")
       * No custodial recovery pending under Sec 23 BSA / Sec 27 Evidence Act
       * No criminal antecedents & deep roots in society (no flight risk)
   - [Part 9] Undertaking to furnish solvent surety and adhere to all bail conditions
   - [Part 10] Prayer Clause (विशिष्ट कानूनी राहत / प्रार्थना)
   - [Part 11] Verification Affidavit (सत्यापन / शपथपत्र) with place, date, applicant signature line, and advocate certification.
"""

# =====================================================================
# Master Multilingual Prompt Constructor
# =====================================================================
def get_multilingual_draft_prompt(
    language: str,
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
    lang_key = language.lower().strip()
    config = INDIAN_LEGAL_LANGUAGES.get(lang_key, INDIAN_LEGAL_LANGUAGES["hindi"])
    native_lang = config["native_name"]
    lang_name = config["name"]

    draft_type_titles = {
        "bail_application": f"Regular Bail Application (BNSS Sec 483 / CrPC Sec 437/439) in {native_lang}",
        "anticipatory_bail": f"Anticipatory Bail Application (BNSS Sec 482 / CrPC Sec 438) in {native_lang}",
        "criminal_complaint": f"Private Criminal Complaint (BNSS Sec 223 / CrPC Sec 200) in {native_lang}",
        "discharge_application": f"Discharge Application (BNSS Sec 250 / CrPC Sec 227/239) in {native_lang}",
        "affidavit": f"Judicial Affidavit / Verification in {native_lang}",
        "exemption_application": f"Exemption Application from Personal Appearance (BNSS Sec 228 / CrPC Sec 205) in {native_lang}",
        "written_arguments": f"Written Arguments & Submissions on behalf of Applicant in {native_lang}"
    }

    selected_title = draft_type_titles.get(draft_type, f"Court Application in {native_lang}")

    rag_block = ""
    if rag_context:
        rag_block = f"\n### 4. RAG Case Precedents & Legal Context:\n{rag_context}\n"

    return f"""Draft a 100% authentic, court-ready criminal legal pleading in standard formal {lang_name} ({native_lang}) for filing in the District & Sessions Court for: '{selected_title}'.

### 1. Case & Court References:
- Court Name: {court_name if court_name else config['default_court']}
- Applicant / Accused Name: {applicant_name if applicant_name else 'Accused / Applicant'}
- Respondent / State: {opponent_name if opponent_name else config['opponent_default']}
- Police Station: {police_station if police_station else config['default_police_station']}
- FIR / Crime Register No. & Year: {fir_number if fir_number else 'FIR No. 184/2024'}
- Statutory Penal Provisions (Sections): {sections if sections else 'Section 420 IPC / Section 318 BNS, Section 35 BNSS'}

### 2. Case Facts & Narrative (Translate into formal court {native_lang}):
{facts}

### 3. Additional Defense Grounds:
{additional_grounds if additional_grounds else 'The applicant is innocent, law-abiding, has no past criminal record, and is falsely implicated without any prima facie evidence.'}
{rag_block}
### Mandatory Requirements:
1. The pleading must be completely in formal, grammatically impeccable judicial {native_lang} ({lang_name}).
2. Include Court Heading, Cause Title, FIR and Sections, Subject Line, Factual Narrative, Substantive Legal Grounds (citing Arnesh Kumar, Satender Antil, Sanjay Chandra), Undertaking, Prayer Clause, and Verification Affidavit.
3. The draft must look ready for physical printing on legal green/white paper for direct court filing.
"""
