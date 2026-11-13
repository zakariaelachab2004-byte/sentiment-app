# Semaine 6 : paquet installable

## Objectif

Faire du dépôt un paquet Python utilisable hors du dossier du projet : une roue installable, une commande `sentiment`, et un modèle lu via la variable `SENTIMENT_MODELE`.

## Ce qui a été mis en place

- package `sentiment_app/`
- point d’entrée `sentiment` défini dans `pyproject.toml`
- version centralisée `0.6.0`
- compatibilité avec les anciens imports `predict`
- import API orienté vers le paquet installé
- génération de la roue avec `python -m build --wheel`

## Vérifications

- `python -m pytest -q` : suite stable
- `sentiment --version` : affiche `sentiment-app 0.6.0`
- `sentiment predict "Livraison rapide, produit conforme, très satisfait"` : retourne un JSON de prédiction valide
- `python -m build --wheel` : construction réussie

## Points clés du TP6

- les tests et les données ne font pas partie du paquet
- le modèle est reconstruit par `python src/train.py`
- le paquet n’utilise pas `sys.path` bricolé dans le code applicatif
- la version est lisible depuis le package et par la commande CLI
- la distribution créée peut être installée dans un environnement neutre

## Livrable final

Le dépôt est désormais en phase de livraison : version identifiée, paquet installable, commande disponible et validation par roue réalisée.
