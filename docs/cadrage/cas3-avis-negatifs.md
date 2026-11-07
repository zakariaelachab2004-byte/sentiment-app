# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Identifier automatiquement les avis clients insatisfaits dès leur publication afin de les router en priorité vers le service support.

## Utilisateur final (obligatoire)
Les agents du service après-vente (SAV) et les responsables de la relation client.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
Nous retenons le Machine Learning classique car nous disposons d'un historique de données étiquetées (a) d'avis clients. De plus, le coût par requête (c) d'un classifieur léger est bien inférieur à celui d'un grand modèle génératif.
## Données nécessaires et leur origine (obligatoire)
Un jeu de données de 20 000 commentaires d'avis clients anonymisés avec leur note de satisfaction associée.

## Métrique de succès et seuil d'acceptation (obligatoire)
Obtenir un F1-score macro d'au moins 0,85 sur la détection des avis insatisfaits.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un avis négatif manqué peut dégrader l'image de marque ; le service client effectue une revue manuelle des avis identifiés comme douteux.

## Risques éthiques ou de confidentialité (obligatoire)
S'assurer de supprimer toutes les données personnelles (noms, téléphones, courriels) contenues dans le texte des avis.

## Approche écartée et pourquoi (facultatif)

