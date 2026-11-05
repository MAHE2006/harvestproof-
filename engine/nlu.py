"""Understands a farmer's short spoken or typed sentence (Tamil or English) as a crop plus symptom answers.

Rule-based on purpose: it is fast, runs offline, never invents anything, and every decision can be traced to the words that caused it.
Precision is preferred over recall: if the words are ambiguous (for example plain "yellow"), nothing is recorded and the app asks a question instead.
"""
import re
import unicodedata

TA = "\u0B80-\u0BFF"
_ZW = dict.fromkeys([0x200B, 0x200C, 0x200D, 0xFEFF])


def norm(text):
    t = unicodedata.normalize("NFC", text or "").translate(_ZW).lower().replace("\u2019", "'")
    t = re.sub(r"[.,;:!?\n\r\u0964|]+", " | ", t)                 # sentence marks become clause separators
    t = re.sub(r"[^a-z0-9'\u0B80-\u0BFF| ]+", " ", t)             # drop emoji and other symbols
    return " " + re.sub(r"\s+", " ", t).strip() + " "


def T(*stems):
    """Tamil word-start match. Tamil adds endings to words, so a stem matches any word beginning with it."""
    return "(?<![" + TA + "])(?:" + "|".join(re.escape(s) for s in stems) + ")"


def E(*words):
    """English word-start match. Words are regex fragments."""
    return r"\b(?:" + "|".join(words) + ")"


def near(a, b, n=3):
    """a and b in the same clause, at most n words apart, in either order (also joined into one word)."""
    gap = r"\S*?(?:\s+(?:\S+\s+){0," + str(n) + "})?"
    return f"(?:{a}){gap}(?:{b})|(?:{b}){gap}(?:{a})"


# (question id, value, regex). Value True = the symptom is present.
RULES = [
    # white powder on top of the leaf
    ("white_powder", True, near(E("white", r"ash\w*", r"flour\w*", r"talc\w*"), E(r"powder\w*", r"dust\w*", r"coating", r"flour\w*"))),
    ("white_powder", True, E(r"powdery", r"talcum")),
    ("white_powder", True, near(T("வெள்ளை", "வெளுத்த", "சாம்பல்"), T("பவுடர்", "பௌடர்", "தூள்", "பொடி", "மாவு"))),
    ("white_powder", True, near(T("பவுடர்", "பௌடர்", "மாவு", "தூள்", "பொடி"), T("போல", "மாதிரி", "போன்ற", "படிந்"), 1)),
    # white fuzzy growth under the leaf
    ("white_fuzz", True, near(E(r"under\w*", "below", "bottom", "back", "lower"), E("white", r"fuzz\w*", r"cotton\w*", r"fluff\w*", "mold", "mould", "fungus"), 5)),
    ("white_fuzz", True, E(r"cottony", r"fluffy white", r"fuzzy white")),
    ("white_fuzz", True, near(T("அடிப்பக்க", "அடியில்", "அடிப்புற", "கீழ்ப்பக்க", "கீழ்ப்புற", "கீழே", "பின்புற", "பின்பக்க"), T("வெள்ளை", "பஞ்சு", "பூஞ்சை"), 4)),
    ("white_fuzz", True, T("பஞ்சு")),
    # curling or puckering
    ("curl", True, E(r"curl\w*", r"twist\w*", r"pucker\w*", r"wrinkl\w*", r"crinkl\w*", r"rolled", r"rolling")),
    ("curl", True, T("சுருட்", "சுருண்", "சுருள", "சுருங்", "சுருக்க")),
    # oily yellow patches
    ("yellow_oily", True, E(r"oily", r"greasy")),
    ("yellow_oily", True, near(E(r"yellow\w*"), E(r"patch\w*", r"blotch\w*"))),
    ("yellow_oily", True, T("எண்ணெய்", "எண்ணை")),
    ("yellow_oily", True, near(T("மஞ்சள்"), T("திட்டு", "கறை"))),
    # round spots with rings
    ("rings", True, r"\b(?:rings?|ringed|concentric|circles)\b"),
    ("rings", True, T("வளைய")),
    # eye / spindle shaped spots
    ("spindle", True, E(r"spindle\w*", r"eye\s+shaped", r"boat\s+shaped", r"diamond\w*", r"lens\s+shaped")),
    ("spindle", True, T("கண் வடிவ", "கண் போன்ற", "கண் போல", "படகு வடிவ", "படகு போன்ற", "நீள்வட்ட", "நீள் வட்ட")),
    # blisters
    ("blister", True, E(r"blister\w*", r"bubbl\w*", r"translucent")),
    ("blister", True, T("கொப்புள", "கொப்பள", "குமிழ்")),
    # rain or humidity in the last week
    ("wet", True, E(r"rain\w*", r"humid\w*", r"damp\w*", r"fog\w*", r"drizzl\w*", r"dew\w*", r"cloudy", r"monsoon", r"wet\s+(?:weather|season|days?|spell)")),
    ("wet", True, T("மழை", "ஈர", "பனி", "மூடுபனி", "மேகமூட்டம்", "தூறல்")),
    ("wet", False, E(r"dry\s+(?:weather|season|spell|days?)", r"drought")),
    ("wet", False, T("வறண்ட", "வறட்சி", "வறள்")),
]
RULES = [(q, v, re.compile(p)) for q, v, p in RULES]

NEG = re.compile(r"\b(?:no|nope|nah|not|without|never|nor|neither|cannot|can't|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|hasn't|haven't|nothing)\b"
                 + "|(?<![" + TA + "])(?:இல்ல|கிடையாது)|வில்லை")
UNSURE = re.compile(r"\b(?:not sure|do not know|don't know|dont know|unsure|not certain|no idea|maybe|perhaps)\b|(?<![" + TA + r"])தெரிய(?:வில்லை|லை|ல|ாது)|(?<![" + TA + "])தெரியாது")
SPLIT = re.compile(r"\s\|\s|\sbut\s|\sஆனால்\s|\sஆனா\s|\sஆனாலும்\s")

CROPS = {
    "rice": [re.compile(r"\b(?:rice|paddy)\b"), re.compile("(?<![" + TA + "])(?:நெல்(?!லிக்)(?!லி(?![" + TA + "]))|நெற்|அரிசி)")],
    "chilli": [re.compile(r"\b(?:chilli|chillies|chili|chilies|chile|chiles|chilly)\b"), re.compile(T("மிளகா", "மொளகா"))],
    "grapes": [re.compile(r"\b(?:grapes?|grapevines?)\b"), re.compile(T("திராட்சை", "திராக்ஷை", "கிரேப்"))],
    "tea": [re.compile(r"\btea\b"), re.compile(T("தேயிலை") + "|(?<![" + TA + "])டீ(?![" + TA + "])")],
}

YES = re.compile(r"\b(?:yes|yeah|yep|yup|correct|true|right|it does|they do|there is|there are|i have|we have)\b|(?<![" + TA + "])(?:ஆம்|ஆமா|ஆமாம்|உண்டு|இருக்கு|இருக்கிறது|இருக்குது|இருக்கின்றன)")


def _gap(clause, a, b):
    """Number of words strictly between character positions a and b (0 if they touch or overlap)."""
    return len(clause[a:b].split()) if b > a else 0


def _negated(clause, matches):
    """Each negation word applies only to its nearest symptom. Tamil negation follows the word it negates,
    English negation usually comes first, so each language looks in its natural direction first."""
    hit = set()
    for n in NEG.finditer(clause):
        tamil = re.search("[" + TA + "]", n.group(0)) is not None
        before = [(i, _gap(clause, m[3], n.start())) for i, m in enumerate(matches) if m[2] <= n.start()]
        after = [(i, _gap(clause, n.end(), m[2])) for i, m in enumerate(matches) if m[2] >= n.end()]
        for group in ((before, after) if tamil else (after, before)):
            group = [(i, g) for i, g in group if g <= 2]
            if group:
                hit.add(min(group, key=lambda x: x[1])[0])
                break
    return hit


def extract(text):
    """Returns {"crops": [...], "symptoms": [{"q", "value", "match"}], "unsure": [...]}."""
    t = norm(text)
    crops = [c for c, pats in CROPS.items() if any(p.search(t) for p in pats)]
    found, unsure = {}, set()
    for clause in SPLIT.split(t):
        clause = f" {clause.strip()} "
        if not clause.strip():
            continue
        matches = [(q, val, m.start(), m.end(), m.group(0).strip()) for q, val, pat in RULES for m in [pat.search(clause)] if m]
        if UNSURE.search(clause):
            unsure.update(m[0] for m in matches)
            continue
        neg = _negated(clause, matches)
        for i, (q, val, _, _, txt) in enumerate(matches):
            found.setdefault(q, []).append((val != (i in neg) if i in neg else val, txt))
    symptoms = []
    for q, items in found.items():
        values = {v for v, _ in items}
        if len(values) == 1:                       # contradictory statements are dropped rather than guessed
            symptoms.append({"q": q, "value": values.pop(), "match": items[0][1]})
    return {"crops": crops, "symptoms": symptoms, "unsure": sorted(unsure - {s["q"] for s in symptoms})}


def parse_yes_no(text):
    """Answer to a yes/no question: "yes", "no", "unsure" or None when unclear."""
    t = norm(text)
    if UNSURE.search(t):
        return "unsure"
    neg, yes = bool(NEG.search(t)), bool(YES.search(t))
    if neg and not yes:
        return "no"
    if yes and not neg:
        return "yes"
    return None
