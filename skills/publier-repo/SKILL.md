---
name: publier-repo
description: À lancer AVANT tout git push (ou toute mise à jour) d'un dépôt public : scanne l'arbre ET tout l'historique à la recherche des noms privés de Nolann (liste hors dépôt), chemins personnels et secrets, puis rappelle le push forcé si l'historique doit être réécrit.
---

# Publier un dépôt sans fuite

1. `bash ~/.claude/skills/publier-repo/scan.sh <dossier du dépôt>` (liste des mots : `mots-interdits.txt`, à créer à côté de `scan.sh`, jamais dans le dépôt).
2. **PROPRE** : on peut pousser normalement.
3. **TROUVÉ dans l'arbre seulement** : corriger le fichier, nouveau commit, push normal.
4. **TROUVÉ dans l'historique** : il faut réécrire (`git filter-branch --tree-filter` + sed, ou `git filter-repo --replace-text`), vérifier avec `scan.sh`, puis **push forcé (`--force-with-lease`) uniquement après le « ok » explicite de Nolann**. Prévenir que les anciens hashs restent visibles côté GitHub un moment (purge = support GitHub).
5. Corriger aussi la source locale (le dossier d'où vient la copie publiée), sinon la prochaine synchronisation remet le nom.
6. Ajouter à `mots-interdits.txt` tout nouveau nom privé rencontré. Ne jamais écrire ces noms dans un dépôt public.
7. Secrets : si `gitleaks` est installé, `gitleaks git` et `gitleaks dir` en complément (MIT).

Piège : `grep -i` sur un mot interdit court peut matcher un mot courant (ex. « adaptation ») ; vérifier la diff avant de conclure à une fuite.
