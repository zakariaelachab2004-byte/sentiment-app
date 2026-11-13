"""Prédiction unitaire : logique de modélisation et configuration de chemins."""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

import joblib

if "predict" in sys.modules and sys.modules["predict"] is not sys.modules[__name__]:
    sys.modules[__name__] = sys.modules["predict"]

RACINE = Path(__file__).resolve().parents[1]
PACKAGE_MODEL = Path(__file__).resolve().parent / "models" / "sentiment.joblib"
REPO_MODEL = RACINE / "models" / "sentiment.joblib"


def chemin_modele() -> Path:
    """Le chemin du modèle est configurable par la variable d'environnement SENTIMENT_MODELE."""
    if modele := os.environ.get("SENTIMENT_MODELE"):
        return Path(modele)
    for candidate in (PACKAGE_MODEL, REPO_MODEL):
        if candidate.exists():
            return candidate
    return PACKAGE_MODEL


MODELE = chemin_modele()


class Resultat(TypedDict):
    """Ce que predict() renvoie : un type précis, que mypy peut suivre."""

    label: str
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle une seule fois par processus."""
    if not MODELE.exists():
        raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
    return joblib.load(MODELE)


def predict(texte: str) -> Resultat:
    """Renvoie {'label': 'positive'|'negative', 'score': float}."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": str(etiquette), "score": round(score, 4)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
