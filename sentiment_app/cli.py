"""Interface en ligne de commande du paquet sentiment_app."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from . import __version__
from .predict import predict


def _version() -> int:
    print(f"sentiment-app {__version__}")
    return 0


def _predict_command(texte: list[str]) -> int:
    text = " ".join(texte)
    resultat = predict(text)
    payload = {"label": resultat["label"].upper(), "score": round(float(resultat["score"]), 4), "text": text}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def _serve() -> int:
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000)
    return 0


def _ui() -> int:
    ui_file = Path(__file__).resolve().parents[1] / "ui" / "app.py"
    if not ui_file.exists():
        raise FileNotFoundError(f"Interface Streamlit introuvable : {ui_file}")
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(ui_file)])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sentiment")
    parser.add_argument("--version", action="store_true", help="Affiche la version du paquet")
    subs = parser.add_subparsers(dest="command")

    predict_parser = subs.add_parser("predict", help="Classifier un texte")
    predict_parser.add_argument("text", nargs="+")

    subs.add_parser("serve", help="Lance l'API FastAPI")
    subs.add_parser("ui", help="Lance l'interface Streamlit")

    args = parser.parse_args(argv)
    if args.version:
        return _version()
    if args.command == "predict":
        return _predict_command(args.text)
    if args.command == "serve":
        return _serve()
    if args.command == "ui":
        return _ui()
    parser.print_help()
    return 0
