# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Détecter automatiquement si une ordonnance numérisée contient toutes les mentions obligatoires avant la délivrance des médicaments.
## Utilisateur final (obligatoire)
Les préparateurs en pharmacie et les pharmaciens lors de la réception de l'ordonnance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
Nous retenons le Machine Learning supervisé car nous disposons d'un historique de données étiquetées (a). De plus, les conséquences d'une erreur (d) sur une ordonnance nécessitent un modèle prédictif évaluable de manière rigoureuse.

## Données nécessaires et leur origine (obligatoire)
Un jeu de données de 5 000 ordonnances anonymisées, annotées avec la présence ou l'absence des mentions obligatoires.

## Métrique de succès et seuil d'acceptation (obligatoire)
Atteindre un rappel (recall) de 98% sur les erreurs d'ordonnance afin de limiter les faux négatifs.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Délivrer un médicament sans la posologie complète, ce qui représente un risque sanitaire pour le patient.

## Risques éthiques ou de confidentialité (obligatoire)
Les ordonnances contiennent des données de santé très sensibles (HIPAA/RGPD) qui doivent être anonymisées.

## Approche écartée et pourquoi (facultatif)

