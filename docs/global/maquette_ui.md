# maquette_ui.md — Sorti du CLAUDE.md le 24/10/2026

Sorti du CLAUDE.md le 24/10/2026 (texte original, mot pour mot ; sauvegarde complète : CLAUDE_avant_menage_2026-10-24.md).

- **Ne pas coder à vue.** Au début d'une appli (ou d'un nouvel écran important) : **architecture + mini maquette**
  avant le code (skills de design, Artifact avec écrans, ou conversation Opus avec captures), validée par moi. Une
  référence (« comme tel autre logiciel ») ne remplace pas la maquette.
  **Barrière (17/10/2026)** : une maquette « belle » se fait en **Opus ultracode**. Sur Sonnet, avant tout travail de
  design : dire « maquette = Opus ultracode », écrire le brief dans `SUIVI.md` et s'arrêter. **Filet** : si une
  maquette a quand même été faite sur Sonnet, le dire en tête du rapport et proposer une passe Opus de retour avant de coder.
  **Première maquette ou changement majeur = Opus ultracode. Changement léger sur une maquette validée = Sonnet puis
  `architecte` relit les captures** ; le rapport donne toujours : captures avant/après côte à côte, liste des
  changements (une ligne chacun), verdict d'`architecte` (2-3 lignes), écarts restants. Sans cela, pas « fait ».
- **Le code doit RESSEMBLER à la maquette validée — règle dure.** Dimensions, espacements, couleurs, textes, ordre,
  états : comme la maquette, pas « dans l'esprit ». **Interdit** de simplifier, remplacer ou laisser tomber un élément
  parce que c'est plus long ou délicat, sans le dire. Une maquette validée est faisable : difficulté technique → **1)
  `architecte` ; 2) poser la question à Nolann** (il préfère changer la maquette que subir un contournement
  silencieux). Tout écart est une **décision à lui**, jamais un choix de Sonnet. Avant « fini » sur un écran :
  **capture côte à côte avec la maquette** et liste des écarts (même vide) dans le rapport / SUIVI.md.
- **Points maquette réguliers** : après un lot de gros changements front + back, ou quand la dernière passe date,
  **me proposer une session Opus ultracode « point maquette »** : lancer la vraie appli, naviguer, prendre des
  captures, vérifier logique et lisibilité, comparer à la maquette et la mettre à jour. Dosage : fin d'un jalon qui
  touche 3 écrans ou plus, ou ajoute un écran ; pas pour une petite correction. L'écrire comme étape dans le plan /
  SUIVI.md d'un chantier d'interface.
- **Avant « fini » sur un écran**, la conversation qui code le lance et le regarde en vrai (Qt :
  `widget.grab().save("x.png")`, même en `offscreen` ; web : navigateur) : lisibilité, alignements, textes coupés,
  états vides et d'erreur. Plus de 2-3 captures → dans un agent. Méthode Qt (captures état par état, contrôle sombre au
  pixel, mesures par introspection) : skill `captures-qt`.
- **Thème sombre de Windows (toutes les applis)** : il casse les interfaces qui se fient aux couleurs du système.
  Toujours fixer soi-même fond **et** texte (Qt : style Fusion + `QPalette` claire explicite + QSS avec `background`
  et `color` sur chaque widget stylé), jamais de couleur « par défaut », et **vérifier chaque nouvel écran, dialogue ou
  popup avec Windows en mode sombre** avant de livrer.

