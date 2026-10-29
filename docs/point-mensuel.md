# Point mensuel : la pipeline bride-t-elle les nouveaux modèles ?

Rendez-vous le 1er de chaque mois, et aussi dès qu'un nouveau modèle sort. Durée visée : 30 min. But : retirer ce qui ne sert plus, pas empiler.

## Check-list
1. Lire les notes de version de Claude Code et des modèles (agent `chercheur`, 1 appel) et les nouveautés notées dans le point hebdo décodeur AI.
2. Relancer UN banc avec la pipeline Claude seule (`executant` Sonnet + vérification). Pas de référence chiffrée depuis le retrait de Codex (22/10/2026) : la première mesure devient la référence.
3. Pour chaque règle « interdit / obligatoire » de `~/.claude/CLAUDE.md` et des agents : refaire une tâche SANS la règle. Si le résultat ne change pas, la supprimer.
4. Vérifier les modèles par défaut (Sonnet 5.5, Opus pour `architecte`) : un nouveau modèle moins cher et aussi bon ?
5. Mettre à jour les dates « mesuré le … » dans CLAUDE.md, la page `results/` du dépôt public, puis lancer le skill `publier-repo` avant tout push.

## Journal (une ligne par point : date, nouveautés, règles retirées, chiffres du banc)
- 17/10/2026 : point initial (ancienne pipeline avec Codex, archive : tag `avec-codex-2026-10-22`).
- 22/10/2026 : Codex retiré, pipeline Claude seule (Max).
