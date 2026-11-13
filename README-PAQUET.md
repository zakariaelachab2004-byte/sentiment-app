# sentiment-app 1.0.0

`sentiment-app` est un paquet Python qui classe en français un avis client comme
`positive` ou `negative`. Il fournit une fonction Python, une commande `sentiment`
et le modèle entraîné embarqué dans la distribution.

## Prérequis

- Python 3.11 ou supérieur
- Un système compatible avec Python

Le paquet contraint scikit-learn à la série 1.5 et utilise joblib 1.4.x, afin de
rester compatible avec le modèle sérialisé inclus.

## Installer la distribution

Depuis le dossier contenant la roue téléchargée depuis la release :

```bash
python -m pip install sentiment_app-1.0.0-py3-none-any.whl
```

Sous Windows, `py -m pip install sentiment_app-1.0.0-py3-none-any.whl` peut être
utilisé à la place de `python -m pip`.

Vérifier l’installation :

```bash
sentiment --version
```

## Utiliser la commande

Classifier un avis :

```bash
sentiment "Livraison rapide et produit conforme"
```

La commande affiche le verdict et un score de prédiction. Pour obtenir une sortie
JSON :

```bash
sentiment --json "Livraison rapide et produit conforme"
```

Exemple de forme de réponse JSON :

```json
{"label": "POSITIVE", "score": 0.8, "text": "Livraison rapide et produit conforme"}
```

Le score indiqué dans cet exemple est illustratif ; le résultat réel dépend du
modèle et du texte fourni.

## Utiliser l’API Python

```python
from sentiment_app.predict import predict

resultat = predict("Livraison rapide et produit conforme")
print(resultat)
```

La fonction renvoie un dictionnaire avec `label` (`positive` ou `negative`) et
`score` (un nombre entre 0 et 1).

## Modèle et configuration

Le fichier du modèle est inclus dans la roue : l’installation ne dépend pas du
dossier du dépôt Git. Par défaut, le paquet charge cette ressource embarquée. La
variable d’environnement `SENTIMENT_MODELE` permet de désigner un autre fichier
modèle ; elle doit être définie avant le démarrage du processus Python.

## Limites et précautions

- Le modèle effectue une classification binaire et ne comprend pas nécessairement
  les nuances, l’ironie, les fautes ou les formulations éloignées de ses données
  d’entraînement.
- Le score correspond à la probabilité maximale renvoyée par le modèle ; il ne
  garantit ni la justesse du verdict ni une confiance calibrée.
- Les performances dépendent de la représentativité des avis d’entraînement.
  Les résultats doivent être contrôlés avant toute décision importante.
- Le modèle est un fichier Joblib sérialisé. N’installez et ne chargez que des
  fichiers provenant d’une source de confiance : la désérialisation de fichiers
  non fiables peut exécuter du code.
