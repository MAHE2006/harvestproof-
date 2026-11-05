"""Tamil (and English) wording for the voice assistant.

NOTE FOR REVIEWERS: these terms were written by an AI model and must be checked by a Tamil-speaking agriculture officer
(for example from TNAU) before real use. Edit the dictionaries below; nothing else needs to change.
"""

CROP = {"rice": ("நெல்", "Rice"), "chilli": ("மிளகாய்", "Chilli"), "grapes": ("திராட்சை", "Grapes"), "tea": ("தேயிலை", "Tea")}

DISEASE = {
    "rice_blast": "நெல் குலை நோய்", "rice_brownspot": "நெல் பழுப்பு இலைப்புள்ளி நோய்", "rice_healthy": "ஆரோக்கியமான நெல் இலை",
    "chilli_cercospora": "மிளகாய் செர்கோஸ்போரா இலைப்புள்ளி நோய்", "chilli_powdery": "மிளகாய் சாம்பல் நோய்", "chilli_murda": "மிளகாய் இலை சுருட்டை (முர்தா) நோய்",
    "chilli_nutritional": "மிளகாய் ஊட்டச்சத்துக் குறைபாடு", "chilli_healthy": "ஆரோக்கியமான மிளகாய் இலை",
    "grapes_downy": "திராட்சை அடிச்சாம்பல் நோய்", "grapes_powdery": "திராட்சை சாம்பல் நோய்", "grapes_healthy": "ஆரோக்கியமான திராட்சை இலை",
    "tea_greyblight": "தேயிலை சாம்பல் கருகல் நோய்", "tea_brownblight": "தேயிலை பழுப்பு கருகல் நோய்", "tea_algalspot": "தேயிலை பாசிப் புள்ளி நோய்",
    "tea_redspot": "தேயிலை சிவப்புப் புள்ளி நோய்", "tea_helopeltis": "தேயிலை கொசு (ஹெலோபெல்டிஸ்) பூச்சித் தாக்கம்", "tea_healthy": "ஆரோக்கியமான தேயிலை இலை",
}

# Yes/no questions, worded so a farmer can answer "ஆம்" or "இல்லை".
QUESTION = {
    "spindle": "இலைப் புள்ளிகள் கண் அல்லது படகு வடிவத்தில், நடுவில் சாம்பல் நிறமும் ஓரத்தில் பழுப்பு நிறமும் உள்ளதா?",
    "rings": "புள்ளிகள் வட்டமாகவும், உள்ளே வளையங்கள் போலவும் உள்ளதா?",
    "yellow_oily": "இலையின் மேல் பக்கம் எண்ணெய் தடவியது போல மஞ்சள் திட்டுகள் உள்ளதா?",
    "white_fuzz": "இலையின் அடிப்பக்கம் வெள்ளை பஞ்சு போன்ற வளர்ச்சி உள்ளதா?",
    "white_powder": "இலையின் மேல் வெள்ளைத் தூள் அல்லது மாவு போன்றது படிந்துள்ளதா?",
    "blister": "புள்ளிகள் ஒளி ஊடுருவும் தன்மையுடன் கொப்புளங்களாக வீங்கியுள்ளதா?",
    "curl": "இலைகள் சுருண்டோ சுருக்கமாகவோ உள்ளதா?",
    "wet": "கடந்த ஒரு வாரத்தில் மழை அல்லது ஈரப்பதமான வெப்பமான வானிலை இருந்ததா?",
}

# Short noun phrases used to show what the app understood from the farmer's sentence.
TOPIC = {
    "spindle": ("கண் வடிவப் புள்ளிகள்", "eye-shaped spots"), "rings": ("வளையப் புள்ளிகள்", "spots with rings"), "yellow_oily": ("எண்ணெய் போன்ற மஞ்சள் திட்டுகள்", "oily yellow patches"),
    "white_fuzz": ("அடிப்பக்கம் வெள்ளை பஞ்சு", "white fuzz underneath"), "white_powder": ("வெள்ளைத் தூள்", "white powder"), "blister": ("கொப்புளங்கள்", "blisters"),
    "curl": ("இலை சுருட்டை", "leaf curl"), "wet": ("மழை அல்லது ஈரப்பதம்", "rain or humidity"),
}

# Problems the official fungicide list does not cover: say why, in plain words.
NO_FUNGICIDE = {
    "chilli_murda": ("இது பூச்சி மற்றும் வைரஸ் தாக்கம். பூஞ்சைக் கொல்லி பயன்படாது. சிலந்திப் பேன், இலைப்பேன் கட்டுப்பாடு பற்றி வேளாண் அதிகாரியிடம் கேளுங்கள்.",
                     "This is a mite, thrips and virus problem. A fungicide does not help. Ask an agriculture officer how to control mites and thrips."),
    "chilli_nutritional": ("இது சத்துக் குறைபாடு போல் தெரிகிறது. பூஞ்சைக் கொல்லி தெளிக்க வேண்டாம். மண் அல்லது இலை பரிசோதனை செய்யுங்கள்.",
                           "This looks like a nutrient problem. Do not spray a fungicide. Get a soil or leaf test."),
    "tea_helopeltis": ("இது பூச்சித் தாக்கம், பூஞ்சைக் கொல்லி பயன்படாது. தேயிலை வாரிய ஆலோசகரிடம் கேளுங்கள்.",
                       "This is an insect pest, so a fungicide does not help. Ask a tea extension officer."),
}
GENERIC_NONE = ("இந்த நோய்க்கு அரசு பூஞ்சைக் கொல்லிப் பட்டியலில் மருந்து இல்லை. வேளாண் அதிகாரியிடம் ஆலோசனை பெறுங்கள். இது ஆலோசனை மட்டுமே.",
                "No fungicide on the official list names this problem. Please consult an agriculture officer. This is advice only.")
ADVICE_ONLY = ("இது ஆலோசனை மட்டுமே.", "This is advice only.")


def _tail(disease, n):
    if n:
        return (f" அரசு பட்டியலில் இந்த நோய்க்கு {n} மருந்துகள் உள்ளன. திரையில் பட்டியலைப் பார்த்து, பேக் குறியீட்டைச் சரிபார்த்து, லேபிளில் உள்ள அளவையும் காத்திருப்பு நாட்களையும் பின்பற்றவும். இது ஆலோசனை மட்டுமே.",
                f" The government label list has {n} spray{'s' if n != 1 else ''} for this problem. Check the list on screen, verify the pack code, and follow the label dose and waiting days. This is advice only.")
    ta, en = NO_FUNGICIDE.get(disease, GENERIC_NONE)
    return " " + ta, " " + en


def compose(status, crop=None, disease=None, disease_en="", p=0.0, question=None, question_en="", n_products=0, suggest_photo=False):
    """Returns (tamil, english) reply text for a voice status."""
    pct = round(p * 100)
    d_ta = DISEASE.get(disease, "")
    q_ta = QUESTION.get(question, "")
    if status == "need_crop":
        return ("எந்தப் பயிர் என்று சொல்லுங்கள்: மிளகாய், தேயிலை, திராட்சை அல்லது நெல்.", "Which crop is it? Say chilli, tea, grapes or rice.")
    if status == "confused":
        return (f"புரியவில்லை. மீண்டும் சொல்லுங்கள், அல்லது இந்தக் கேள்விக்குப் பதில் சொல்லுங்கள். {q_ta} 'ஆம்', 'இல்லை' அல்லது 'தெரியவில்லை' என்று சொல்லவும்.",
                f"I did not understand. Please say it again, or answer this question. {question_en} Say yes, no or not sure.")
    if status == "asking":
        return (f"இன்னும் உறுதியாகத் தெரியவில்லை. {q_ta} 'ஆம்', 'இல்லை' அல்லது 'தெரியவில்லை' என்று சொல்லவும்.", f"I am not sure yet. {question_en} Say yes, no or not sure.")
    if status == "uncertain":
        return ("இந்த விவரங்களை வைத்து நோயைச் சொல்ல முடியவில்லை. இலையை வேளாண் அதிகாரியிடம் காட்டுங்கள்.", "I cannot tell the disease from these details. Please show the leaf to an agriculture officer.")
    if status == "healthy":
        return ("இலை ஆரோக்கியமாகத் தெரிகிறது. மருந்து தெளிக்கத் தேவையில்லை.", "The leaf looks healthy. No spray is needed.")
    t_ta, t_en = _tail(disease, n_products)
    if suggest_photo:
        t_ta, t_en = " புகைப்படமும் எடுத்தால் உறுதி கூடும்." + t_ta, " A photo of the leaf will make this more certain." + t_en
    if status == "confident":
        return (f"{d_ta} போல் தெரிகிறது. உறுதி {pct} சதவீதம்." + t_ta, f"This looks like {disease_en.lower()}. {pct}% sure." + t_en)
    if status == "leading":
        return (f"{d_ta} ஆக இருக்கலாம். உறுதி {pct} சதவீதம் மட்டுமே, முழுமையாக உறுதியில்லை." + t_ta, f"It may be {disease_en.lower()}. Only {pct}% sure, so this is not certain." + t_en)
    raise ValueError(status)
