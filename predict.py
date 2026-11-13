"""Compatibilité historique du module `predict`.

Les tests du TP2/TP4 importent `predict` directement ; cette version garde le même
comportement tout en rendant le paquet installable `sentiment_app` compatible avec
le même objet de module.
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import TypedDict

import joblib

# Les anciens tests patchent `predict.MODELE` et appellent `predict.charger_modele()`.
# On aligne aussi le nom du paquet installable sur ce même module.
RACINE = Path(__file__).resolve().parent


def chemin_modele() -> Path:
    if modele := os.environ.get("SENTIMENT_MODELE"):
        return Path(modele)
    return RACINE / "models" / "sentiment.joblib"


MODELE = chemin_modele()
sys.modules["sentiment_app.predict"] = sys.modules[__name__]


class Resultat(TypedDict):
    label: str
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    if not MODELE.exists():
        raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
    return joblib.load(MODELE)


def predict(texte: str) -> Resultat:
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


__all__ = ["Resultat", "MODELE", "charger_modele", "main", "predict"]

if __name__ == "__main__":
    raise SystemExit(main())
