# Compte rendu TP2 — modèle de sentiment

Le jeu reproductible contient 290 avis (80 positifs, 80 négatifs, 100 mitigés et 30 neutres); sur les 58 avis de test, le vocabulaire contient 316 termes, le F1 macro vaut **0,879** et la matrice est `[[27, 2], [5, 24]]`.

Les sept erreurs du test portent toutes sur des avis mitigés.
Le modèle TF-IDF compte les mots positifs et négatifs sans comprendre que la conclusion de l'avis inverse parfois le sentiment.
Pour réduire ces erreurs, il faudrait mieux modéliser l'ordre et le contexte des mots et ajouter des avis mitigés variés à l'entraînement.

Le modèle reste local dans `models/sentiment.joblib`; les mesures sont enregistrées dans `models/metrics.json`. `python src/train.py --allocine` a aussi été vérifié sur les 20 000 avis Allociné : F1 macro **0,920** sur les 4 000 avis de test.
