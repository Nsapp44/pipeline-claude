---
name: menage-claude-md
description: Réduire le CLAUDE.md d'un projet sous ~15 Ko sans rien perdre (déplacer le détail dans docs/). À lancer quand le hook signale qu'il est trop gros, ou en fin de chantier.
---

# Ménage du CLAUDE.md d'un projet

**Exclu : le CLAUDE.md global (`~/.claude/CLAUDE.md`) n'est JAMAIS traité par ce skill** (décision de Nolann, 12/10) ; seulement les CLAUDE.md de projets. Si on te le demande pour le global, refuser et le rappeler.

But : CLAUDE.md ≤ 15 Ko (≈ 150 lignes de 100 caractères), relu à chaque message ; **rien de perdu**.

1. Pas pendant qu'un workflow ou un agent écrit dans le fichier : attendre sa fin.
2. Lancer l'agent **`architecte`** (le seul agent Opus) avec la recette ci-dessous (le tri demande du jugement : une décision
   de l'utilisateur perdue coûte cher). Lui donner le chemin du CLAUDE.md et les docs existantes du projet.
3. Relire son résultat (diff) moi-même, puis dire en une ligne à l'utilisateur : avant / après (Ko) et où est parti le reste.

## Recette pour l'agent

- **Garder dans CLAUDE.md** : présentation (3 lignes), règles de travail et interdits, pièges et leçons techniques,
  décisions **encore à construire** ou qui contraignent tout le projet, liste de ce qui n'est **pas fiable**,
  comment lancer / tester (court), pointeurs vers `docs/`.
- **Déplacer dans `docs/`** (le journal technique du projet, sinon `docs/JOURNAL_TECHNIQUE.md` ; ou la spec si elle
  existe) : décisions déjà codées et leur détail, historique, architecture détaillée, résultats de validation.
  **Déplacer, ne jamais supprimer** ; sous un titre daté « Sorti du CLAUDE.md le JJ/MM/AAAA ».
- Une ligne par sujet, pas de redite entre sections, phrases courtes.
- Contrôle avant de rendre : chaque phrase retirée se retrouve dans `docs/` (vérifier par recherche de mots-clés
  distinctifs) ; taille finale mesurée ; rapport court : tailles avant / après, ce qui est parti où, doutes éventuels.
- Pas de commit. En cas de doute sur ce qu'on peut sortir : le laisser et le signaler.
- Si ça ne converge pas (2-3 essais), s'arrêter et rendre la main avec le point de blocage.
