from __future__ import annotations

import os
import re
import subprocess
import tempfile
import venv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, env=env, check=False)


def fail(message: str) -> None:
    print(f"[ECHEC] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


wheel_files = sorted(DIST.glob("*.whl"))
if not wheel_files:
    fail("aucune roue trouvée dans dist/")
wheel = wheel_files[-1]
ok(f"roue trouvée : {wheel.name}")

with zipfile.ZipFile(wheel) as archive:
    names = archive.namelist()
    required = [
        "sentiment_app/__init__.py",
        "sentiment_app/cli.py",
        "sentiment_app/predict.py",
        "sentiment_app/models/sentiment.joblib",
    ]
    missing = [item for item in required if item not in names]
    if missing:
        fail(f"ressources manquantes dans la roue : {missing}")
ok("modèle embarqué dans la roue")

changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
if "[1.0.0]" not in changelog:
    fail("CHANGELOG.md ne décrit pas la version [1.0.0]")
ok("CHANGELOG.md décrit la version 1.0.0")

version_match = re.search(r'"version"\s*:\s*"([^\"]+)"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"))
if not version_match or version_match.group(1) != "1.0.0":
    fail("version du paquet dans pyproject.toml doit être 1.0.0")
ok("version pyproject.toml = 1.0.0")

with tempfile.TemporaryDirectory(prefix="sentiment-livrable-") as tmp_dir:
    venv_dir = Path(tmp_dir) / "venv"
    venv.EnvBuilder(with_pip=True).create(venv_dir)
    python_bin = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    pip_install = run([str(python_bin), "-m", "pip", "install", "--upgrade", "pip", "pytest"], ROOT)
    if pip_install.returncode != 0:
        fail(f"échec de l'installation de pip/pytest :\n{pip_install.stdout}\n{pip_install.stderr}")

    wheel_install = run([str(python_bin), "-m", "pip", "install", str(wheel)], ROOT)
    if wheel_install.returncode != 0:
        fail(f"échec de l'installation de la roue :\n{wheel_install.stdout}\n{wheel_install.stderr}")
    ok("installation de la roue dans un environnement neuf")

    env = os.environ.copy()
    env["VERIFICATION_LIVRABLE"] = "1"
    tests = run([str(python_bin), "-m", "pytest", str(ROOT / "tests" / "test_paquet.py"), "-q"], ROOT, env=env)
    if tests.returncode != 0:
        fail(f"tests du paquet installés en échec :\n{tests.stdout}\n{tests.stderr}")
    ok("tests du paquet installés = OK")

    cli_version = run([str(python_bin), "-m", "sentiment_app", "--version"], ROOT, env=env)
    if cli_version.returncode != 0:
        fail(f"commande installée non fonctionnelle :\n{cli_version.stdout}\n{cli_version.stderr}")
    ok("commande installée : " + cli_version.stdout.strip())

    cli_predict = run([str(python_bin), "-m", "sentiment_app", "Excellent produit, très satisfait"], ROOT, env=env)
    if cli_predict.returncode != 0:
        fail(f"commande de prédiction en échec :\n{cli_predict.stdout}\n{cli_predict.stderr}")
    ok("prédiction CLI OK")

    git_tag = run(["git", "tag", "--list", "v1.0.0"], ROOT)
    if git_tag.returncode != 0 or "v1.0.0" not in git_tag.stdout.splitlines():
        fail("tag Git v1.0.0 absent")
    ok("tag Git v1.0.0 présent")

print("Bilan : CONFORME")
