# Compte rendu TP3 — API FastAPI

L'API refuse de démarrer sans modèle afin de signaler immédiatement un déploiement incomplet : elle ne doit ni prétendre être prête ni répondre avec un modèle de remplacement. Une erreur de validation dans le schéma et une validation dans `predict()` sont volontairement redondantes : l'API protège son contrat HTTP et la fonction TP2 reste sûre lorsqu'elle est appelée ailleurs.

`GET /health` confirme que le modèle est effectivement chargé. `POST /predict` renvoie un verdict, une confiance et le texte soumis; les erreurs d'entrée sont des 422, l'absence du modèle est une 503 et une panne interne est une 500 sans détail sensible.

Vérifications manuelles T15 à T20 effectuées par Membre B :
- T15 (GET /health) : 200 OK avec modèle tfidf-logreg
- T16 (POST /predict positif) : 200 POSITIVE
- T17 (POST /predict négatif) : 200 NEGATIVE
- T18 (requêtes invalides) : 422 Unprocessable Entity
- T20 (sans modèle) : refus de démarrage immédiat avec FileNotFoundError
