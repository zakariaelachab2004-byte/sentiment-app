"""Compatibilité historique pour les tests du TP2/TP4.

Les anciennes importations `from predict import ...` et `python src/predict.py ...`
restent valides en pointant vers le module installé `sentiment_app.predict`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sentiment_app import predict as _module  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(_module.main())

sys.modules[__name__] = _module
