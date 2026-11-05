"""Evidence-fusion diagnosis: trained photo likelihoods + question answers, with information-gain question choice."""
import csv, math, pathlib, sys
import joblib
import numpy as np
try:
    import sklearn._loss._loss
    if "_loss" not in sys.modules:
        sys.modules["_loss"] = sklearn._loss._loss
except ImportError:
    pass
from .features import FEATURES

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA, MODELS = ROOT / "data", ROOT / "models"


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(r for r in f if not r.startswith("#")))


def entropy(p):
    p = np.asarray(p)
    return float(-(p[p > 0] * np.log2(p[p > 0])).sum())


class Model:
    def __init__(self, img=None, path=None):
        self.classes = {r["class_id"]: {"crop": r["crop"], "name": r["name"], "prior": float(r["prior"])} for r in read_csv(DATA / "classes.csv")}
        self.questions = {r["question"]: r["text"] for r in read_csv(DATA / "questions.csv")}
        self.qlik = {}
        for r in read_csv(DATA / "question_likelihoods.csv"):
            self.qlik.setdefault(r["class_id"], {})[r["question"]] = float(r["p_yes"])
        p = pathlib.Path(path) if path else MODELS / "image_model.joblib"
        # Only load model files that you trained yourself: joblib files can run code when loaded.
        self.img = img or (joblib.load(p) if p.exists() else None)
        # Precomputed once: class ids per crop, log priors, and per-question likelihood vectors.
        self._ids, self._prior, self._q = {}, {}, {}
        for c, v in self.classes.items():
            self._ids.setdefault(v["crop"], []).append(c)
        for crop, ids in self._ids.items():
            self._prior[crop] = np.log([self.classes[c]["prior"] for c in ids])
            raw = {q: np.array([self.qlik[c][q] for c in ids]) for q in self.questions}
            clipped = {q: np.clip(raw[q], 1e-3, 1 - 1e-3) for q in raw}
            self._q[crop] = {q: (raw[q], np.log(clipped[q]), np.log(1 - clipped[q])) for q in raw}

    @property
    def trained(self):
        return bool(self.img)

    def crop_trained(self, crop):
        return bool(self.img) and crop in self.img["crops"]

    @property
    def trained_crops(self):
        return sorted(self.img["crops"]) if self.img else []

    def accept_for(self, crop):
        return (self.img or {}).get("meta", {}).get("accept", {}).get(crop, .8)

    def _base(self, crop, feats, use_img=True):
        """Log prior plus photo evidence. The photo classifier runs here, once per request."""
        ids = self._ids.get(crop)
        if not ids:
            raise ValueError("unknown crop")
        lp = self._prior[crop].copy()
        if use_img and feats and self.crop_trained(crop):
            m = self.img["crops"][crop]
            pr = dict(zip(m["classes"], m["clf"].predict_proba([[feats.get(f, 0.0) for f in FEATURES]])[0]))
            lp += np.array([math.log(max(pr.get(c, 0.0), 1e-6)) for c in ids]) / m["T"]
        return ids, lp

    def _fuse(self, crop, lp, answers):
        for q, a in (answers or {}).items():
            if a is None or q not in self.questions:
                continue
            lp = lp + (self._q[crop][q][1] if a else self._q[crop][q][2])
        e = np.exp(lp - lp.max())
        return e / e.sum()

    def posterior(self, crop, feats=None, answers=None, use_img=True):
        ids, lp = self._base(crop, feats, use_img)
        e = self._fuse(crop, lp, answers)
        return sorted(zip(ids, e.tolist()), key=lambda x: -x[1])

    def _best_question(self, crop, lp0, answers, skip=()):
        p0 = self._fuse(crop, lp0, answers)
        base = entropy(p0)
        best = None
        for q in self.questions:
            if q in answers or q in skip:
                continue
            py = float((p0 * self._q[crop][q][0]).sum())
            hy = entropy(self._fuse(crop, lp0, {**answers, q: True}))
            hn = entropy(self._fuse(crop, lp0, {**answers, q: False}))
            g = base - py * hy - (1 - py) * hn
            if best is None or g > best["gain"]:
                best = {"question": q, "text": self.questions[q], "gain": round(g, 4)}
        return best if best and best["gain"] > 1e-3 else None

    def next_question(self, crop, feats, answers, skip=()):
        """The unanswered question with the highest expected entropy reduction."""
        _, lp0 = self._base(crop, feats)
        return self._best_question(crop, lp0, answers or {}, skip)

    def analyse(self, crop, feats, answers, skip=()):
        """Everything a request needs from ONE run of the photo classifier: posterior, photo-only posterior, next question."""
        ids, lp0 = self._base(crop, feats)
        answers = answers or {}
        pairs = lambda e: sorted(zip(ids, e.tolist()), key=lambda x: -x[1])
        photo_only = pairs(self._fuse(crop, lp0, None)) if feats and self.crop_trained(crop) else None
        return pairs(self._fuse(crop, lp0, answers)), photo_only, self._best_question(crop, lp0, answers, skip)

    def verdict(self, post, has_next, crop, photo_used=True):
        """The per-crop threshold was tuned on photo-only validation, so it applies only when a photo was used. Answers alone use 0.8."""
        c, p = post[0]
        if p >= (self.accept_for(crop) if photo_used else .8):
            return {"status": "confident", "id": c, "p": p}
        if has_next:
            return {"status": "asking", "id": c, "p": p}
        return {"status": "leading" if p >= .6 else "uncertain", "id": c if p >= .6 else None, "p": p}
