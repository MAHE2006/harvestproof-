# HarvestProof

Speak or show a leaf, check a pesticide pack, choose a spray that fits your harvest date, and give buyers a signed harvest passport.
**New: ask by voice in Tamil or English and hear the answer read back in Tamil.**

## Project layout
| Folder | What it is |
|---|---|
| `frontend/` | **React** app (Vite). Source code you edit. |
| `web/` | The built React app. The Python server serves this, so you do not need Node just to run the project. |
| `api/` | **Backend** (FastAPI): login, voice, diagnosis, pack checks, planner, passport. `db.py` holds the database tables. |
| `engine/` | AI: leaf photo measurements, trained model, question choosing, Tamil/English language understanding (`nlu.py`), Tamil wording (`tamil.py`), planner. |
| `models/` | The trained photo model (tea and chilli) and its accuracy report. |
| `data/` | Products, label doses and waiting days, symptom questions. |
| `tests/`, `frontend/src/test/`, `frontend/e2e/` | Automated tests (see below). |

Tech stack: Python 3.12, FastAPI, SQLModel (SQLite, or PostgreSQL with `DATABASE_URL`), scikit-learn, React 18, Vite. No neural network, no paid AI service.

## Run it (VS Code terminal)
```bash
python -m venv .venv
.venv\Scripts\activate                 # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
set HP_SECRET=put-a-long-random-string-here        # Mac/Linux: export HP_SECRET=...
python -m uvicorn api.main:app --reload
```
Open http://localhost:8000 and press **Start the demo**. If you used an older version of this project, delete its `harvestproof.db` first.

To change the React app (needs Node 18+):
```bash
cd frontend
npm install
npm run dev        # http://localhost:5173, talks to the Python server on port 8000
npm run build      # writes the production app into ../web
```

## Ask by voice
1. Step 1 has a microphone panel. Choose Tamil or English, tap the microphone, and say, for example, **"My chilli leaves have white powder"** or **"என் மிளகாய் இலையில் வெள்ளை பவுடர் இருக்கு"**.
2. The browser turns your speech into text (you can correct it in the box). The server finds the **crop** and the **symptoms**, including negatives ("no rain", "மழை இல்லை") and "not sure", then works out the likely disease.
3. The answer appears in Tamil and English and is **read aloud in Tamil**. If it is not sure yet, it asks a yes/no question in Tamil. Answer by voice ("ஆம்", "இல்லை", "தெரியவில்லை") or tap the buttons.
4. Photos and voice can be mixed. Saying a different crop starts over for that crop.

What you need, and what can go wrong:
- **Browser:** Chrome (Android or computer) or Edge. Firefox has no speech recognition. Speech recognition needs **https or localhost**. On a phone over plain `http://192.168...` the microphone is disabled by the browser, but typing still works.
- **Internet:** Chrome sends the audio to Google to turn it into text, so voice input needs internet. The diagnosis itself runs on your server.
- **Tamil voice:** reading aloud in Tamil needs a Tamil text-to-speech voice on the phone. Most Android phones have one (Settings, Language, Text-to-speech, Google). If none is found, the app says so and still shows the Tamil text.
- **Recognition mistakes:** Tamil speech recognition is not perfect, so the app always shows what it heard and lets the farmer correct it.
- **I could not test with a real microphone or a real Tamil voice.** Those parts were tested with simulated ones. Please try it on a real phone.
- **Tamil wording** (disease names, questions, replies in `engine/tamil.py`) was written by an AI. Have a Tamil-speaking agriculture officer review it. Edit the file and nothing else needs to change.
- It understands a fixed set of symptoms (white powder, white fuzz underneath, curling, oily yellow patches, rings, eye-shaped spots, blisters, rain or humidity). Unclear words such as plain "yellow" are deliberately not guessed: the app asks a question instead.

## Tests
```bash
python -m pytest tests -q                        # 61 backend tests (language understanding, voice, packs, planner, passport, security)
cd frontend && npm test                          # 14 tests of the voice panel and the app, with a simulated microphone and speaker
node frontend/e2e/e2e.cjs http://localhost:8000 bundle.js   # full journey against a running server (see the file header)
```
The end-to-end script runs the real app through a farmer's whole journey (24 checks): voice in Tamil and English, crop switching, follow-up questions, forged/cloned/expired packs, spray plan, logging, shareable passport, photo samples.

## What is real, and what is not
| Part | Status |
|---|---|
| Photo model, **tea** (6 classes) | Trained on public photos. On 822 held-out photos: **76.5% right**, well calibrated. Called "confident" for 60% of photos, and right 88.5% of those. |
| Photo model, **chilli** (5 classes) | Only 532 photos. On 79 held-out photos: **56% right**. A chilli photo alone is never "confident", so the app asks questions. |
| **Rice and grapes** | No photo model. They work from answers (typed, tapped or spoken). |
| Voice understanding | Rule-based, tested on 46 Tamil and English cases. It has **not** been measured on real farmers' speech. |
| Symptom probabilities (`data/question_likelihoods.csv`) | **My estimates**, not survey data. They drive the diagnosis from answers and voice. Replace with field survey data. |
| Products, doses, waiting days (26 fungicides) | Real CIB&RC rows, transcribed by hand. Verify against the official list and the label. |
| EU residue limits | Only 4 chilli products. Others show "not recorded". |
| Pack registry | Codes you issue are fully verified. A manufacturer's registry needs their data (`scripts/import_batches.py`). |

Diagnosing from answers alone is "confident" at 80%. The app then says a photo will make it more certain. Nothing here has been field-tested with an agronomist.

## What was optimised
- **AI speed:** choosing the next question took 137 ms because the photo model was re-run 17 times. It now runs once: **12 ms**, with identical results (checked on 6 cases).
- **One classifier run per request** instead of three.
- **Database:** the spray planner used about 52 queries per request (two per product). It now uses 3 bulk queries, and the passport loads products and labels once. Label and disease columns are indexed.
- **Measured on this server:** photo diagnosis 31 ms, voice request 6.5 ms, spray plan 5 ms.
- **Photos are shrunk in the browser** (to 1280 px) before upload, so a 5 MB phone photo uploads as a few hundred KB.
- **Web app:** production React bundle is 60 kB compressed, responses are gzip-compressed.
- **Safety:** rate limits on login, sign-up, verify, diagnose and voice (`api/ratelimit.py`). Behind a proxy, run uvicorn with `--proxy-headers`. For several server processes use a shared limiter at the proxy.
- **Bugs fixed:** the old page used the UTC date (a day behind in the early morning in India); dates now use the farmer's local time and the server allows one day of slack. "Try again" after a failed load works. "Not sure" answers are never asked twice.

## Pack codes
```bash
python -m scripts.issue TRICY75 B2603 --count 100        # product codes are in data/products.csv; prints signed codes
python -m scripts.import_batches registry.csv            # columns: batch_code,product_code,mfg,exp
```
Imported batches are checked by registry lookup only (no signature); write their codes as `BATCH-SERIAL-NA`. Manufacturers' registries are not public: you need an agreement with them or the regulator.
Demo batches exist only while `HP_DEMO=1`. **Set `HP_DEMO=0` in production.**

## Retrain with your own photos
```bash
python -m scripts.fetch_data                  # public tea + chilli photos into data/images/<class_id>/
# add your own photos to the same folders, with the diagnosis confirmed by an agronomist
python -m engine.train --data data/images --workers 4     # about 8 minutes for 6,400 photos
```
Read `models/report.json` before trusting a new model, then restart the server. `models/image_model.joblib` can run code when loaded, so only load files you trained yourself.

## Deploy
Set `HP_SECRET` (long and random), `HP_DEMO=0` and `DATABASE_URL`. `docker build -t harvestproof . && docker run -p 8000:8000 -e HP_SECRET=... -e HP_DEMO=0 harvestproof`.
Use HTTPS (camera, QR scanning and the microphone all need it), run uvicorn with `--proxy-headers` behind a proxy, and back up the database.
Delete `harvestproof.db` after editing the label CSVs, which are only read when the database is first created.

## Limits
Advice, not a laboratory certificate. Have an agronomist confirm diagnoses on your farms, and have a lab test residues, before using a passport as proof with buyers.
