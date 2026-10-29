# Configuration stable Claude Code (05/10/2026) — à copier sur l'autre abonnement

## Fichiers à copier (dans ~/.claude/)
| Fichier | Rôle |
|---|---|
| `CLAUDE.md` | règles d'économie (efforts, agents, contexte, pauses) |
| `agents/lecteur.md` (Haiku), `agents/chercheur.md`, `agents/executant.md` (Sonnet) | agents légers |
| `agents/architecte.md` (Opus, high) | seul agent Opus, pour un point très dur dans une conversation Sonnet |
| `hooks/claude_md_taille.py` | alerte CLAUDE.md de projet trop gros |
| `hooks/pause_longue.py` | bloque le 1er message après > 1 h de pause si contexte > 80 k (renvoyer = passe) |
| `hooks/conso_5h.py` | barre d'état conso (terminal seulement, ne tourne pas dans l'appli) |
| `skills/menage-claude-md/` | ménage d'un CLAUDE.md trop gros |

## settings.json : ne PAS copier le fichier entier, reporter seulement ces clés
```json
"model": "sonnet",
"advisorModel": "fable",
"autoCompactWindow": 160000,
"workflowSizeGuideline": "small",
"modelSettings": {
  "claude-opus-5-5":   { "effortLevel": "medium" },
  "claude-sonnet-5-5": { "effortLevel": "medium" }
},
"env": { "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1", "BASH_MAX_OUTPUT_LENGTH": "15000" },
"permissions": { "deny": ["CronCreate","CronDelete","CronList","RemoteTrigger","PushNotification",
  "NotebookEdit","EnterWorktree","ExitWorktree",
  "Agent(general-purpose)","Agent(claude)","Agent(Plan)"] },
"statusLine": { "type": "command", "command": "\"<python.exe>\" \"<…>/.claude/hooks/conso_5h.py\"" },
"hooks": { "UserPromptSubmit": [ { "hooks": [ { "type": "command",
  "command": "\"<python.exe>\" \"<…>/.claude/hooks/claude_md_taille.py\"" },
  { "type": "command", "command": "\"<python.exe>\" \"<…>/.claude/hooks/pause_longue.py\"" } ] } ] }
```
À adapter : chemins `~/.claude` et `C:/Python314/python.exe`.
À NE PAS copier : `permissions.allow` (règles de ce PC, dont des cookies de session de sites locaux) et les hooks
`claude-office-hook.exe` (outil propre à ce PC ; à remettre seulement s'il est installé là-bas).
Ne pas mettre `subagentPromptCacheTtl: "1h"` (plus cher, voir plus bas).

## Plugins
Les plugins synchronisés depuis claude.ai (design, searchfit-seo, engineering, prisma…) ne se coupent PAS par
projet : les désactiver dans claude.ai (Customize > plugins) s'ils ne servent pas → ~-5 k créés par session.

## Ce qu'on économise (mesures de docs/mesures.md, équivalent Opus)
| Règle | Gain mesuré |
|---|---|
| Agents légers (lecteur/chercheur/executant) au lieu de general-purpose | ~5× moins cher par agent |
| Grep + plages de lignes au lieu de lire un gros fichier en entier | 4,4× moins (220 k → 50 k) |
| Consigne d'agent précise (fichiers, lignes, « 10 lignes max ») | ~2× moins cher par agent |
| Nouvelle conversation + passation au lieu de /compact | ~30 k au lieu de ~108 k |
| Ne pas changer d'effort/modèle en cours de conversation | évite de recréer tout le contexte (2× sa taille) |
| Effort medium au lieu de high | même résultat aux tests (26/26), -50 % de réflexion |
| Agents Sonnet en medium (clé corrigée `claude-sonnet-5-5`) | réflexion ~5-6 k au lieu de 8-11 k en xhigh |
| Agent qui n'attend jamais > 5 min | 22 % du cache des agents perdu sur un projet Qt (≈1,1 M) |
| Pas de reprise après > 1 h dans une conversation lourde | 23 % du cache du fil perdu sur 14 jours ici |
| Cache 1 h des agents NON activé | aurait coûté +2,6 M pour 1,1 M économisés |
| Sorties de commande coupées (BASH_MAX_OUTPUT_LENGTH 15000) | une sortie de 10 Ko = +30 % sur le tour |

Bugs de cache Anthropic : vérifié avec `quota/cache_casse.py` → cassures inexpliquées ≈ 4 % du cache créé
(surtout des sessions de test en ligne de commande) ; l'outil tiers claude-code-cache-fix n'est pas utile ici.
À lancer aussi sur l'autre PC : `python cache_casse.py 14`.

## Modèle principal : Sonnet par défaut (05/10)
| Tâche (tests cachés) | Opus medium | Sonnet medium |
|---|---|---|
| Évaluateur d'expressions | 26/26, ~56-101 k | 26/26, 27-56 k |
| Lecteur CSV (33 cas, erreurs) | 33/33, 52 k | 33/33, 27 k |
→ ~45-50 % moins cher à qualité égale. Opus : conversation dédiée à l'architecture (choisi au démarrage, ultracode),
ou agent `architecte` pour un point dur ponctuel ; advisor Fable avant les deux.
