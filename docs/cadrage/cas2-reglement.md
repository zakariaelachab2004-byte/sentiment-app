# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Permettre aux juristes et responsables de conformité d'interroger rapidement l'ensemble des textes de loi et réglementations internes mis à jour.
## Utilisateur final (obligatoire)
L'équipe juridique, les auditeurs internes et les responsables de la conformité réglementaire de l'entreprise.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

L'approche RAG est choisie pour assurer une parfaite vérifiabilité (b) des réponses en citant directement les articles de loi sources. De plus, elle réduit le coût par requête (c) par rapport au réentraînement complet d'un modèle génératif.
## Données nécessaires et leur origine (obligatoire)
L'ensemble des documents réglementaires, procédures internes et textes de loi au format PDF issus de la base documentaire juridique.

## Métrique de succès et seuil d'acceptation (obligatoire)
Obtenir un taux de précision d'au moins 95 % sur la pertinence des articles et références juridiques restitués.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une fausse interprétation juridique peut entraîner des sanctions financières ; une validation humaine par un juriste reste obligatoire avant toute prise de décision.

## Risques éthiques ou de confidentialité (obligatoire)
Risque d'accès non autorisé à des documents confidentiels d'entreprise si les droits d'accès à la base vectorielle ne sont pas strictement cloisonnés.

## Approche écartée et pourquoi (facultatif)

