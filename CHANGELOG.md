# Changelog

## [0.6.0] - 2026-11-13

### Ajouté
- paquet Python installable `sentiment_app`
- CLI `sentiment` avec commandes `--version`, `predict`, `serve` et `ui`
- version centralisée dans `sentiment_app.__version__`
- compatibilité historique pour les imports `predict` du TP2/TP4
- validation de la roue construite hors du dépôt

### Modifié
- `api/model.py` importe désormais le paquet `sentiment_app.predict`
- `pyproject.toml` décrit les dépendances et les points d'entrée du package
- `requirements-dev.txt` inclut `build`

## [0.1.0] - 2026-11-13

### Ajouté
- structure initiale du dépôt
- environnement Python et dépendances du projet
- application de démonstration, API FastAPI, interface Streamlit et tests
