import os, io, json, tempfile
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.mkdtemp(), "t.db")
os.environ["HP_SECRET"] = "test-secret"
os.environ["HP_DEMO"] = "1"
import numpy as np
from datetime import date, timedelta
from fastapi.testclient import TestClient
from scripts.make_demo_data import make
from api.main import app, eu_info


def hdr(c, email="a@x.com"):
    r = c.post("/api/register", json={"email": email, "password": "longpassword", "name": "Asha", "district": "Madurai"})
    assert r.status_code == 200, r.text
    return {"Authorization": "Bearer " + r.json()["token"]}


def test_eu_info():
    assert eu_info(None)["level"] == "unknown" and eu_info(.01)["level"] == "strict" and eu_info(3.0)["level"] == "ok"


def test_full_flow():
    with TestClient(app) as c:
        assert c.post("/api/diagnose", data={"crop": "rice"}).status_code == 401
        h = hdr(c)
        assert c.post("/api/register", json={"email": "a@x.com", "password": "longpassword"}).status_code == 409
        assert c.post("/api/login", json={"email": "a@x.com", "password": "bad"}).status_code == 401
        assert c.post("/api/login", json={"email": "a@x.com", "password": "longpassword"}).status_code == 200
        t = date.today()
        # demo codes behave as labelled
        demo = {d["kind"]: d["code"] for d in c.get("/api/demo-codes", headers=h).json()}
        g = c.post("/api/verify", headers=h, json={"code": demo["genuine"]}).json()
        assert g["ok"] and [k["name"] for k in g["checks"]] == ["Code format", "Registered batch", "Signature", "Not expired", "Scan pattern"] and all(k["ok"] for k in g["checks"])
        assert "expired" in c.post("/api/verify", headers=h, json={"code": demo["expired"]}).json()["title"].lower()
        assert "signature" in c.post("/api/verify", headers=h, json={"code": demo["forged"]}).json()["title"].lower()
        assert "cloned" in c.post("/api/verify", headers=h, json={"code": demo["cloned"]}).json()["title"].lower()
        assert c.post("/api/verify", headers=h, json={"code": "NOPE-00001-AAAAAAAA"}).json()["title"] == "This batch is not registered"
        # issue codes (first user is admin) and verify one
        codes = c.post("/api/admin/issue", headers=h, json={"product_code": "TRICY75", "batch": "t1", "mfg": str(t - timedelta(days=5)), "exp": str(t + timedelta(days=500)), "count": 3}).json()["codes"]
        good = codes[0]
        assert c.post("/api/verify", headers=h, json={"code": good}).json()["product_code"] == "TRICY75"
        bad = good[:-1] + ("A" if good[-1] != "A" else "B")
        assert not c.post("/api/verify", headers=h, json={"code": bad}).json()["ok"]
        # diagnose: questions only, photo on a trained crop and an untrained crop
        r = c.post("/api/diagnose", headers=h, data={"crop": "grapes", "answers": "{}"}).json()
        assert r["next"] and len(r["posterior"]) == 3 and not r["photo_trained"]
        first = c.post("/api/diagnose", headers=h, data={"crop": "grapes", "answers": "{}"}).json()["next"]["question"]
        r = c.post("/api/diagnose", headers=h, data={"crop": "grapes", "answers": json.dumps({first: None})}).json()
        assert r["next"]["question"] != first and r["answered"] == 0     # 'not sure' is never asked twice
        r = c.post("/api/diagnose", headers=h, data={"crop": "grapes", "answers": '{"yellow_oily":true,"white_fuzz":true}'}).json()
        assert r["verdict"]["status"] == "confident" and r["verdict"]["id"] == "grapes_downy"
        buf = io.BytesIO(); make("tea_greyblight", np.random.default_rng(1)).save(buf, "JPEG")
        r = c.post("/api/diagnose", headers=h, data={"crop": "tea", "answers": "{}"}, files={"image": ("l.jpg", buf.getvalue(), "image/jpeg")}).json()
        assert r["features"] and r["photo_used"] and r["photo_only"] and len(r["posterior"]) == 6
        assert c.post("/api/diagnose", headers=h, data={"crop": "rice"}, files={"image": ("x.jpg", b"notanimage", "image/jpeg")}).status_code == 422
        # plan: only products whose label lists the problem; harvest date filters
        p = c.post("/api/plan", headers=h, json={"crop": "rice", "disease": "rice_blast", "harvest": str(t + timedelta(days=40))}).json()["options"]
        assert p[0]["recommended"] and p[0]["wait"] <= 12 and all(o["code"] != "AZOX23" for o in p)
        assert any(o["code"] == "ISOPRO40" and "too late" in o["why"] for o in p)
        assert not any(o["recommended"] for o in c.post("/api/plan", headers=h, json={"crop": "rice", "disease": "rice_blast", "harvest": str(t + timedelta(days=3))}).json()["options"])
        assert c.post("/api/plan", headers=h, json={"crop": "rice", "disease": "rice_healthy"}).json()["no_spray"]
        assert c.post("/api/plan", headers=h, json={"crop": "chilli", "disease": "chilli_murda"}).json()["options"] == []
        # log sprays: wrong crop, future date, forged code rejected
        base = {"field": "Plot 1", "crop": "grapes", "code": good, "sprayed": str(t)}
        assert c.post("/api/sprays", headers=h, json=base).status_code == 422
        assert c.post("/api/sprays", headers=h, json={**base, "crop": "rice", "sprayed": str(t + timedelta(days=2))}).status_code == 422
        assert c.post("/api/sprays", headers=h, json={**base, "crop": "rice", "code": bad}).status_code == 422
        assert c.post("/api/sprays", headers=h, json={**base, "crop": "rice", "sprayed": str(t - timedelta(days=10))}).status_code == 200
        g = c.get("/api/passport", headers=h).json()["groups"][0]
        assert g["clear"] == str(t - timedelta(days=10) + timedelta(days=30)) and g["hold_days"] == 20 and g["export_warning"]
        # a later rotation: same mode of action as the last spray is ruled out
        p = c.post("/api/plan", headers=h, json={"crop": "rice", "disease": "rice_blast", "field": "Plot 1"}).json()
        assert any(o["code"] == "TRICY75" and "mode of action" in o["why"] for o in p["options"])
        # share and signature
        tok = c.post("/api/passport/share", headers=h, json={"field": "Plot 1", "crop": "rice"}).json()["token"]
        pub = c.get(f"/api/public/passport/{tok}").json()
        assert c.post("/api/public/passport/check", json=pub).json()["valid"]
        pub["payload"] = pub["payload"].replace("Asha", "Bob")
        assert not c.post("/api/public/passport/check", json=pub).json()["valid"]
        # isolation between users
        h2 = hdr(c, "b@x.com")
        assert c.get("/api/passport", headers=h2).json()["groups"] == []
        assert c.delete(f"/api/sprays/{g['sprays'][0]['id']}", headers=h2).status_code == 404
        assert c.post("/api/admin/issue", headers=h2, json={"product_code": "TRICY75", "batch": "z", "mfg": str(t), "exp": str(t), "count": 1}).status_code == 403
        assert c.get("/api/qr.png?text=hello").headers["content-type"] == "image/png"


def test_sample_photos_and_static_pages():
    import pathlib
    from api.main import WEB
    with TestClient(app) as c:
        h = hdr(c, "s@x.com")
        for name, crop in [("tea_greyblight", "tea"), ("chilli_powdery", "chilli")]:
            img = (WEB / "samples" / f"{name}.jpg").read_bytes()
            r = c.post("/api/diagnose", headers=h, data={"crop": crop, "answers": "{}"}, files={"image": ("s.jpg", img, "image/jpeg")}).json()
            assert r["photo_used"] and r["photo_only"] and abs(sum(x["p"] for x in r["posterior"]) - 1) < 1e-3 and r["verdict"]["status"] in ("confident", "asking", "leading", "uncertain")
        assert "HarvestProof" in c.get("/").text and c.get("/samples/tea_healthy.jpg").status_code == 200
        assert c.get("/p/abc").status_code == 200 and c.get("/api/meta").json()["photo_model"]["trained_crops"] == ["chilli", "tea"]


def test_voice_conversation_english_and_tamil():
    from api.ratelimit import limiter
    limiter.reset()
    with TestClient(app) as c:
        h = hdr(c, "v1@x.com")
        say = lambda text, **kw: c.post("/api/voice", headers=h, json={"text": text, "lang": kw.pop("lang", "ta"), **kw}).json()
        # the headline example, in English
        r = say("My chilli leaves have white powder.", lang="en")
        assert r["crop"] == "chilli" and r["status"] == "confident" and r["diagnosis"]["verdict"]["id"] == "chilli_powdery"
        assert r["heard"][0]["q"] == "white_powder" and r["answers"] == {"white_powder": True}
        assert "மிளகாய் சாம்பல் நோய் போல் தெரிகிறது" in r["reply"]["ta"] and "சதவீதம்" in r["reply"]["ta"] and "12 மருந்துகள்" in r["reply"]["ta"] and "புகைப்படமும் எடுத்தால்" in r["reply"]["ta"]
        assert "powdery mildew" in r["reply"]["en"] and len(r["options"]) == 3 and r["options"][0]["wait"] <= r["options"][-1]["wait"] + 30
        # the same in Tamil
        r = say("எனது மிளகாய் இலைகளில் வெள்ளை பவுடர் இருக்கு")
        assert r["crop"] == "chilli" and r["diagnosis"]["verdict"]["id"] == "chilli_powdery" and r["reply"]["status"] == "confident"
        # a dialogue: crop only, then yes/no answers, with 'not sure' never repeated
        r = say("தேயிலை")
        assert r["crop"] == "tea" and r["status"] == "asking" and r["pending"] and r["reply"]["ta"].count("ஆம்") >= 1
        asked = [r["pending"]]
        for reply in ["தெரியவில்லை", "இல்லை", "no", "yes"]:
            r = say(reply, crop="tea", answers=r["answers"], pending=r["pending"])
            if not r["pending"]:
                break
            assert r["pending"] not in asked
            asked.append(r["pending"])
        assert r["crop"] == "tea" and r["status"] in ("asking", "leading", "confident", "uncertain", "healthy")
        # a different crop mid-conversation discards the old answers
        r = say("grape leaves have white powder", crop="tea", answers={"rings": True})
        assert r["crop"] == "grapes" and r["answers"] == {"white_powder": True} and r["diagnosis"]["verdict"]["id"] == "grapes_powdery"
        # explicit statement beats a yes/no for the pending question
        r = say("இல்லை, வெள்ளை பவுடர் இருக்கு", crop="chilli", answers={}, pending="curl")
        assert r["answers"] == {"white_powder": True}
        # no crop, two crops, gibberish, empty
        assert say("hello")["status"] == "need_crop" and "எந்தப் பயிர்" in say("hello")["reply"]["ta"]
        assert say("chilli and tea have problems")["status"] == "need_crop"
        r = say("blah blah", crop="chilli")
        assert r["status"] == "confused" and r["pending"] and "புரியவில்லை" in r["reply"]["ta"]
        assert c.post("/api/voice", headers=h, json={"text": "   "}).status_code == 422
        assert c.post("/api/voice", headers=h, json={"text": "x" * 501}).status_code == 422
        assert c.post("/api/voice", json={"text": "hi"}).status_code == 401
        # healthy and no-fungicide cases speak sensibly
        r = say("tea leaf looks fine, no spots, no rings, no rain", crop="tea", answers={"rings": False, "spindle": False, "blister": False, "wet": False, "yellow_oily": False, "white_powder": False, "curl": False, "white_fuzz": False})
        assert r["status"] in ("healthy", "confident", "leading", "uncertain")
        r = say("மிளகாய் இலை சுருண்டு இருக்கு")                   # curl alone is only ~78% murda, below the 80% bar: the app must ask, not declare
        assert r["status"] == "asking" and r["diagnosis"]["verdict"]["id"] == "chilli_murda" and r["pending"]
        r = say("வெள்ளை பவுடர் இல்லை", crop="chilli", answers=r["answers"], pending=r["pending"])      # now ~84%
        assert r["status"] == "confident" and r["diagnosis"]["verdict"]["id"] == "chilli_murda" and r["options"] == []
        assert "பூஞ்சைக் கொல்லி பயன்படாது" in r["reply"]["ta"]


def test_diagnose_now_also_returns_a_tamil_reply_and_rate_limit_works():
    from api.ratelimit import limiter
    limiter.reset()
    with TestClient(app) as c:
        h = hdr(c, "v2@x.com")
        r = c.post("/api/diagnose", headers=h, data={"crop": "grapes", "answers": '{"yellow_oily":true,"white_fuzz":true}'}).json()
        assert r["reply"]["status"] == "confident" and "திராட்சை அடிச்சாம்பல் நோய்" in r["reply"]["ta"]
        limiter.reset()
        codes = [c.post("/api/login", json={"email": "v2@x.com", "password": "wrongpass"}).status_code for _ in range(12)]
        assert codes[:10] == [401] * 10 and codes[10:] == [429, 429]
        limiter.reset()
        assert c.post("/api/login", json={"email": "v2@x.com", "password": "longpassword"}).status_code == 200


def test_time_zone_slack_for_local_dates():
    with TestClient(app) as c:
        c.post("/api/register", json={"email": "a@x.com", "password": "longpassword"})           # the first account in a database is the admin
        h = {"Authorization": "Bearer " + c.post("/api/login", json={"email": "a@x.com", "password": "longpassword"}).json()["token"]}
        t = date.today()
        code = c.post("/api/admin/issue", headers=h, json={"product_code": "TRICY75", "batch": "tz1", "mfg": str(t), "exp": str(t + timedelta(days=300)), "count": 1}).json()["codes"][0]
        base = {"field": "F", "crop": "rice", "code": code}
        assert c.post("/api/sprays", headers=h, json={**base, "sprayed": str(t + timedelta(days=1))}).status_code == 200      # farmer's tomorrow-in-UTC is accepted
        assert c.post("/api/sprays", headers=h, json={**base, "sprayed": str(t + timedelta(days=2))}).status_code == 422
        o = c.post("/api/plan", headers=h, json={"crop": "rice", "disease": "rice_blast", "today": str(t + timedelta(days=1))}).json()["options"][0]
        assert o["earliest"] == str(t + timedelta(days=1 + o["wait"]))                                                          # uses the farmer's own date
        o = c.post("/api/plan", headers=h, json={"crop": "rice", "disease": "rice_blast", "today": str(t + timedelta(days=30))}).json()["options"][0]
        assert o["earliest"] == str(t + timedelta(days=o["wait"]))                                                              # absurd dates are ignored
