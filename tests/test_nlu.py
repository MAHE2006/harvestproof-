import pytest
from engine import nlu, tamil
from engine.model import Model

m = Model()


def got(text):
    r = nlu.extract(text)
    return r["crops"], {s["q"]: s["value"] for s in r["symptoms"]}, r["unsure"]


def test_the_example_sentence():
    assert got("My chilli leaves have white powder.") == (["chilli"], {"white_powder": True}, [])


@pytest.mark.parametrize("text,crop,syms", [
    ("எனது மிளகாய் இலைகளில் வெள்ளை பவுடர் இருக்கு", "chilli", {"white_powder": True}),
    ("மிளகாய் இலையில் வெள்ளைத் தூள் படிந்திருக்கு", "chilli", {"white_powder": True}),
    ("மிளகாய் இலை மேல பவுடர் தூவினது மாதிரி இருக்கு", "chilli", {"white_powder": True}),
    ("நெல் இலை சுருண்டு போச்சு, மழை இல்லை", "rice", {"curl": True, "wet": False}),
    ("மழை இல்லாமல் இலை சுருண்டு இருக்கு", None, {"curl": True, "wet": False}),
    ("மிளகாய் இலை சுருளவில்லை", "chilli", {"curl": False}),
    ("இலையின் அடிப்பக்கம் வெள்ளை பூஞ்சை இருக்கு", None, {"white_fuzz": True}),
    ("திராட்சை இலையில் எண்ணெய் போல மஞ்சள் திட்டு", "grapes", {"yellow_oily": True}),
    ("தேயிலை இலையில் கொப்புளங்கள் வந்திருக்கு", "tea", {"blister": True}),
    ("நெல்லில் குலை நோய்", "rice", {}),
    ("grape leaves have yellow oily patches and white fuzz under the leaf", "grapes", {"yellow_oily": True, "white_fuzz": True}),
    ("tea leaves have rings but no rain", "tea", {"rings": True, "wet": False}),
    ("there is no rain and leaves are curled", None, {"curl": True, "wet": False}),
    ("no white powder, leaves are curled", None, {"white_powder": False, "curl": True}),
    ("leaves don't have curling", None, {"curl": False}),
    ("white powder is not there", None, {"white_powder": False}),
    ("paddy leaves have eye shaped spots", "rice", {"spindle": True}),
    ("it was humid and rainy this week", None, {"wet": True}),
])
def test_understands(text, crop, syms):
    crops, s, _ = got(text)
    assert crops == ([crop] if crop else []) and s == syms


@pytest.mark.parametrize("text", ["my leaves are yellow", "நெல்லிக்காய் மரத்தில் புழு", "அடிக்கடி இலை உதிருது", "வெள்ளை ஈ தொல்லை", "hello", "", "   ", "🌶️🌶️"])
def test_ambiguous_or_irrelevant_records_nothing(text):
    crops, s, _ = got(text)
    assert s == {} and "rice" not in crops


def test_unsure_and_contradiction_are_not_guessed():
    assert got("chilli leaves curled, not sure about rain") == (["chilli"], {"curl": True}, ["wet"])
    assert got("it rained last week, no rain today")[1] == {}


def test_two_crops_are_reported_so_the_app_can_ask():
    assert set(got("chilli and tea both have problems")[0]) == {"chilli", "tea"}


@pytest.mark.parametrize("text,ans", [("yes", "yes"), ("yeah there is", "yes"), ("ஆம்", "yes"), ("ஆமாம் இருக்கு", "yes"), ("இருக்கு", "yes"), ("no", "no"), ("nope", "no"), ("இல்லை", "no"), ("இல்லீங்க", "no"),
                                      ("தெரியவில்லை", "unsure"), ("தெரியலை", "unsure"), ("not sure", "unsure"), ("maybe", "unsure"), ("hello", None), ("yes no", None)])
def test_yes_no(text, ans):
    assert nlu.parse_yes_no(text) == ans


def test_every_class_and_question_has_tamil_text():
    for cid in m.classes:
        assert tamil.DISEASE.get(cid), cid
    for q in m.questions:
        assert tamil.QUESTION.get(q) and tamil.TOPIC.get(q), q
    for crop in {v["crop"] for v in m.classes.values()}:
        assert tamil.CROP[crop][0]
    for st in ["need_crop", "confused", "asking", "uncertain", "healthy", "confident", "leading"]:
        ta, en = tamil.compose(st, "chilli", "chilli_powdery", "Chilli powdery mildew", .82, "curl", "Leaf is curled", 5)
        assert ta and en and "{" not in ta + en
    assert "82 சதவீதம்" in tamil.compose("confident", "chilli", "chilli_powdery", "Chilli powdery mildew", .82, None, "", 5)[0]


def test_nlu_question_ids_exist_in_the_model():
    assert {q for q, _, _ in nlu.RULES} <= set(m.questions)
