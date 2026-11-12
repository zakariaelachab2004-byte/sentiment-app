# Compte rendu TP5 — interface Streamlit

L'interface n'importe ni le modèle ni la fonction de prédiction : elle appelle le client HTTP, qui transmet les demandes à l'API. Ainsi, réentraîner le modèle ne demande aucune modification de la page.

Quand la confiance est sous 0,60, la page affiche « Je ne sais pas » et demande une vérification humaine au lieu de forcer une classe. Pour un texte de confiance, les exemples du guide donnent « Avis positif » à 78 % et « Avis négatif » à 75 %.

Si l'API ne répond plus, la page indique qu'elle est injoignable et demande de démarrer `uvicorn api.main:app`. Un texte composé d'espaces est signalé comme refusé.

Le fichier `data/avis_exemple.csv` permet de tester l'onglet de lot : six avis sont présentés avec leur verdict et leur confiance, le résumé attendu est `{'POSITIVE': 3, 'NEGATIVE': 2, 'INDETERMINE': 1}`, et le bouton télécharge `resultats.csv`.
