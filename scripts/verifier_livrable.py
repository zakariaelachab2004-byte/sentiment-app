from __future__ import annotations

import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import venv
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
REPORT = ROOT / "docs" / "livrable-tp4.txt"
RESULTS: list[str] = []


def write_report(bilan: str, message: str | None = None) -> None:
    lines = [
        "Rapport de vérification du livrable TP4",
        "Projet : sentiment-app",
        "Version : 1.0.0",
        f"Date : {date.today().isoformat()}",
        "",
        "Contrôles :",
        *RESULTS,
    ]
    if message:
        lines.append(f"[ECHEC] {message}")
    lines.extend(["", f"Bilan : {bilan}"])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


write_report("EN COURS")


def run(
    cmd: list[str], cwd: Path, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, env=env, check=False)


def fail(message: str) -> None:
    print(f"[ECHEC] {message}")
    write_report("NON CONFORME", message)
    raise SystemExit(1)


def ok(message: str) -> None:
    result = f"[OK] {message}"
    RESULTS.append(result)
    print(result)


expected_artifacts = {
    "sentiment_app-1.0.0-py3-none-any.whl",
    "sentiment_app-1.0.0.tar.gz",
}
actual_artifacts = {path.name for path in DIST.iterdir()} if DIST.exists() else set()
if actual_artifacts != expected_artifacts:
    fail(
        "dist/ doit contenir exactement la roue 1.0.0 et l'archive source 1.0.0 ; "
        f"contenu trouvé : {sorted(actual_artifacts)}"
    )
wheel = DIST / "sentiment_app-1.0.0-py3-none-any.whl"
source = DIST / "sentiment_app-1.0.0.tar.gz"
ok(f"roue présente : {wheel.name}")
ok(f"distribution source présente : {source.name}")

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
    if any(name.startswith("tests/") for name in names):
        fail("la roue ne doit pas contenir le dossier tests/")
ok("modèle embarqué dans la roue")
ok("aucun test embarqué dans la roue")

with tarfile.open(source, "r:gz") as archive:
    source_names = archive.getnames()
    required_source_files = [
        "sentiment_app-1.0.0/pyproject.toml",
        "sentiment_app-1.0.0/README-PAQUET.md",
        "sentiment_app-1.0.0/sentiment_app/models/sentiment.joblib",
    ]
    missing_source = [item for item in required_source_files if item not in source_names]
    if missing_source:
        fail(f"fichiers manquants dans la distribution source : {missing_source}")
ok("README et modèle présents dans la distribution source")

changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
if "[1.0.0]" not in changelog:
    fail("CHANGELOG.md ne décrit pas la version [1.0.0]")
ok("CHANGELOG.md décrit la version 1.0.0")

version_match = re.search(r'^version\s*=\s*"([^"]+)"\s*$', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.MULTILINE)
if not version_match or version_match.group(1) != "1.0.0":
    fail("version du paquet dans pyproject.toml doit être 1.0.0")
ok("version pyproject.toml = 1.0.0")

with tempfile.TemporaryDirectory(prefix="sentiment-livrable-") as tmp_dir:
    verification_dir = Path(tmp_dir)
    venv_dir = verification_dir / "venv"
    venv.EnvBuilder(with_pip=True).create(venv_dir)
    python_bin = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    env = os.environ.copy()
    for key in ("PYTHONHOME", "PYTHONPATH", "PYTHONUSERBASE", "PYTHONSTARTUP"):
        env.pop(key, None)
    env["PYTHONNOUSERSITE"] = "1"

    pip_install = run(
        [str(python_bin), "-m", "pip", "install", "--upgrade", "pip", "pytest"],
        verification_dir,
        env,
    )
    if pip_install.returncode != 0:
        fail(f"échec de l'installation de pip/pytest :\n{pip_install.stdout}\n{pip_install.stderr}")

    wheel_install = run(
        [str(python_bin), "-m", "pip", "install", str(wheel)],
        verification_dir,
        env,
    )
    if wheel_install.returncode != 0:
        fail(f"échec de l'installation de la roue :\n{wheel_install.stdout}\n{wheel_install.stderr}")
    ok("installation de la roue dans un environnement neuf")

    import_probe = run(
        [
            str(python_bin),
            "-c",
            (
                "from pathlib import Path; import sentiment_app; "
                "module = Path(sentiment_app.__file__).resolve(); "
                "assert any(part.lower() == 'site-packages' for part in module.parts), module; "
                "print(module)"
            ),
        ],
        verification_dir,
        env,
    )
    if import_probe.returncode != 0:
        fail(f"le paquet n'est pas importé depuis site-packages :\n{import_probe.stderr}")
    ok("module importé depuis site-packages : " + import_probe.stdout.strip())

    package_test = verification_dir / "test_paquet.py"
    shutil.copy2(ROOT / "tests" / "test_paquet.py", package_test)
    tests = run(
        [str(python_bin), "-m", "pytest", str(package_test), "-q"],
        verification_dir,
        env,
    )
    if tests.returncode != 0:
        fail(f"tests du paquet installés en échec :\n{tests.stdout}\n{tests.stderr}")
    ok(f"tests du paquet installés : {tests.stdout.strip()}")

    command = shutil.which(
        "sentiment",
        path=str(venv_dir / ("Scripts" if os.name == "nt" else "bin")),
    )
    if command is None:
        fail("commande installée `sentiment` introuvable dans l'environnement neuf")

    cli_version = run([command, "--version"], verification_dir, env)
    if cli_version.returncode != 0:
        fail(f"commande installée non fonctionnelle :\n{cli_version.stdout}\n{cli_version.stderr}")
    ok("commande installée : " + cli_version.stdout.strip())

    cli_predict = run(
        [command, "Excellent produit, très satisfait", "--json"],
        verification_dir,
        env,
    )
    if cli_predict.returncode != 0:
        fail(f"commande de prédiction en échec :\n{cli_predict.stdout}\n{cli_predict.stderr}")
    ok("prédiction CLI : " + cli_predict.stdout.strip())

    git_tag = run(["git", "rev-parse", "v1.0.0^{commit}"], ROOT)
    git_head = run(["git", "rev-parse", "HEAD"], ROOT)
    if git_tag.returncode != 0 or git_tag.stdout.strip() != git_head.stdout.strip():
        fail("le tag Git v1.0.0 doit pointer sur le dernier commit")
    ok("tag Git v1.0.0 sur le dernier commit")

write_report("CONFORME")
print("Bilan : CONFORME")
print(f"Rapport : {REPORT.relative_to(ROOT)}")
