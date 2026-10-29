# Alléger un SUIVI.md : mesures (28/10/2026)

Test : mêmes 10 questions posées à un sous-agent Haiku qui ne lit que les fichiers autorisés ; justesse comparée à des réponses attendues ; coût = tokens de l'agent. Quatre SUIVI de projets différents.

| SUIVI | original | v2 | v3 (léger + archive) |
|---|---|---|---|
| A | 29,4 k | 30,2 k | 34,5 k |
| B | 27,9 k | 29,9 k | 35,5 k |
| C | 29,7 k | 28,5 k | 32,2 k |
| D | 24,7 k | 26,5 k | - |

Justesse : v1 (très allégé) 6-9 sur 10 ; v2 10/10 partout. Aucune version n'est moins chère que l'original.

## Conclusions
- Un SUIVI déjà dense ne devient pas moins cher en le compressant. Le gain n'existe que pour un fichier qui accumule de l'historique.
- Le coût réel vient du contexte traîné, des compactions et des pauses > 1 h, pas de la relecture par message : 0 à 11 lectures du SUIVI sur 174 à 15 181 messages dans les 12 plus grosses conversations.
- Règles retenues : lire le SUIVI une fois ; un SUIVI par chantier ; fiche `docs/chantiers/<chantier>.md` pour reprendre plus tard ; hook `hooks/suivi_taille.py` (alerte > 8 Ko, une fois par conversation).
- Risque observé : un allègement a fait perdre une info (ordre d'une liste). D'où la règle « zéro perte » : déplacer sans réécrire, garder valeurs exactes, listes ordonnées et un index des archives.
- Limite du hook : ne reconnaît que `SUIVI.md` et `docs/SUIVI.md`.
