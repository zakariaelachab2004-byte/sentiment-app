import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_spec = importlib.util.find_spec("sentiment_app")
_package_installed = bool(_spec and "site-packages" in (_spec.origin or "").lower())
if not _package_installed and not os.environ.get("VERIFICATION_LIVRABLE"):
    pytest.skip("paquet non installé : python scripts/verifier_livrable.py", allow_module_level=True)

import sentiment_app  # noqa: E402
from sentiment_app.predict import predict  # noqa: E402


def test_importe_depuis_le_paquet_installe() -> None:
    assert _package_installed, (
        f"sentiment_app doit venir de site-packages, pas de {sentiment_app.__file__}"
    )


def test_version_paquet() -> None:
    assert sentiment_app.__version__ == "1.0.0"


def test_predict_installe() -> None:
    resultat = predict("Excellent produit, très satisfait")
    assert set(resultat) == {"label", "score"}
    assert resultat["label"] in {"positive", "negative"}
    assert 0.0 <= float(resultat["score"]) <= 1.0


def test_commande_installee() -> None:
    command = shutil.which("sentiment", path=str(Path(sys.executable).parent))
    assert command is not None
    completed = subprocess.run([command, "--version"], capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "sentiment-app 1.0.0" in completed.stdout

    prediction = subprocess.run(
        [command, "Excellent produit, très satisfait", "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert prediction.returncode == 0, prediction.stderr
    assert '"label":' in prediction.stdout
