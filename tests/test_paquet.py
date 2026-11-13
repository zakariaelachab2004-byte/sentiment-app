import importlib.util
import os
import shutil
import subprocess
import sys

import pytest

_spec = importlib.util.find_spec("sentiment_app")
if not (_spec and "site-packages" in (_spec.origin or "")) and not os.environ.get("VERIFICATION_LIVRABLE"):
    pytest.skip("paquet non installé : python scripts/verifier_livrable.py", allow_module_level=True)

import sentiment_app  # noqa: E402
from sentiment_app.predict import predict  # noqa: E402


def test_version_paquet() -> None:
    assert sentiment_app.__version__ == "1.0.0"


def test_predict_installe() -> None:
    resultat = predict("Excellent produit, très satisfait")
    assert set(resultat) == {"label", "score"}
    assert resultat["label"] in {"positive", "negative"}
    assert 0.0 <= float(resultat["score"]) <= 1.0


def test_commande_installee() -> None:
    assert shutil.which("sentiment") is not None
    completed = subprocess.run([sys.executable, "-m", "sentiment_app", "--version"], capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "sentiment-app 1.0.0" in completed.stdout
