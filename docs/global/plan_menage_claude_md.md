# Plan de ménage du CLAUDE.md global (proposition, rien n'est appliqué)

Mesuré le 24/10/2026 : `~/.claude/CLAUDE.md` = 25 917 octets, 8 sections. Cible ≤ 15 Ko.
Principe : rien n'est supprimé ; tout détail sorti part dans `~/.claude/docs/` avec une ligne de renvoi.

## 1. Tableau section par section

| Section (taille actuelle) | Décision | Après |
|---|---|---|
| Économie de tokens et modes d'effort (11,6 Ko) | Garder les règles, sortir mesures/prix/bancs/détails | ~6,3 Ko |
| - Modes d'effort (medium/high/ultra) | Résumer en 3 lignes (sans les « mesuré ») | |
| - Modèle principal, architecte, qui fait quoi | Résumer en 4 lignes ; mesures (0,08 $, 45-50 %, 2-3×) → `docs/agents_delegation.md` | |
| - Déclencheurs d'architecte (1 à 6) | GARDER ENTIER (sauf « bancs T9 16/10 » → docs) | |
| - Si je suis absent / changement d'effort = cache | Résumer en 2 lignes | |
| - Sous-agents gradués + Nombre d'agents + Choisir l'agent | Fusionner en 1 tableau de 5 lignes (Haiku/Sonnet/agents, nombres) | |
| - Relectures sur demande + consigne de revue de code | Déplacer la consigne de revue mot pour mot → `docs/agents_delegation.md` ; 1 ligne de renvoi | |
| - Contrat de fin de délégation | Garder 2 lignes (livrable = message final ; arrêt après 3 mêmes erreurs) ; détail lecteur 0-1 → docs | |
| - Règles d'agents 24/10 (kill python, testeur, chercheur indispo) | Déplacer → `docs/agents_delegation.md`, garder « jamais kill de tous les python.exe » en 1 ligne | |
| - Rafale / dictée + lot d'interface | Fusionner dans « File des demandes » (1re ligne « j'ai compris ») ; checklist interface → section Maquette | |
| - Délégation OBLIGATOIRE (+ seuil, relire la diff, annoncer) | GARDER le noyau ; chiffres de mesure du seuil → docs | |
| - Agent n'attend pas > 5 min + plafond 100 k caractères | Garder 3 lignes (5 min, un livrable, ~30 appels, plafond 100 k → scinder) ; calcul 270 k/160 k → docs | |
| - Agent qui galère demande conseil | Garder 2 lignes | |
| - Planifier PowerShell / routine Claude | Déplacer → `docs/planification_routines.md`, 1 ligne | |
| - Pas d'agent de surveillance / Monitor | Garder 2 lignes ; détail → `docs/planification_routines.md` | |
| Contexte court (6,1 Ko) | | ~3,8 Ko |
| - File des demandes | GARDER ENTIER (+ fusion Rafale) | |
| - Doute = pop-up | GARDER ENTIER | |
| - Compaction / fin de sujet / compaction stratégique | Garder règles (fin de sujet, /compact aux frontières) en 3 lignes ; liste des frontières → `docs/contexte_cache.md` | |
| - Coût fixe 78 k (mesures) | Résumer 1 ligne (« pas de MCP sans besoin, mon accord avant de toucher aux réglages ») ; chiffres → docs | |
| - Jamais changer de conversation pendant un chantier | Garder 2 lignes | |
| - Pause > 1 h | Garder 1 ligne (« pause » = SUIVI.md avant) ; fonctionnement du hook → docs | |
| - SUIVI.md | GARDER le noyau (état courant, rubriques, réécrit avant chaque compte rendu) ; « vécu 12/10 », 33 Ko → docs | |
| - Contexte léger + Docs d'abord | Fusionner en 2 lignes (redite avec « lecteur ≥ 3 fichiers ») | |
| - CLAUDE.md projet 15 Ko + hook | Garder 1 ligne | |
| - Interdit de contourner | GARDER ENTIER (« 3 fois sur 3 » → docs possible) | |
| État des lieux (1,5 Ko) | GARDER, compacter les 2 premiers points en 1 | ~1,2 Ko |
| Maquette / interfaces (3,3 Ko) | Garder barrière Opus ultracode, « ressembler à la maquette », thème sombre ; points maquette réguliers + méthode captures → `docs/maquette_ui.md` | ~2,0 Ko |
| Vidéo / motion (0,9 Ko) | 2 lignes ; détails Nasap3D/Éclat → `docs/video_motion.md` | ~0,35 Ko |
| Produit physique (0,3 Ko) | Garder tel quel (déjà un renvoi) | 0,27 Ko |
| Codex / OpenAI (1,2 Ko) | 2 lignes ; historique tags, fin novembre → `docs/codex_illustrations.md` ; « Échelle d'un bug » = redite des déclencheurs, à retirer de là | ~0,4 Ko |
| Skills (1,0 Ko) | Garder 3 lignes (registre-config, proposer un skill, leçons) | ~0,7 Ko |
| **Total** | | **~15 Ko** (marge : en-têtes, liens) |

Nouveaux fichiers docs/ : `agents_delegation.md`, `planification_routines.md`, `contexte_cache.md`, `maquette_ui.md`,
`video_motion.md`, `codex_illustrations.md` (existants gardés : `mascotte_oeil_oracle.md`, `produit_physique_cao.md`).

## 2. Lignes de renvoi qui restent dans CLAUDE.md

- `- Mesures (prix, bancs, cache des agents), consigne de revue de code à coller, règles d'agents du 24/10 : ~/.claude/docs/agents_delegation.md (à lire avant de rédiger une consigne de revue ou un prompt d'agent long).`
- `- Planifier/relancer un travail = Planificateur de tâches Windows (script .ps1) ; rendez-vous réguliers de veille = routine Claude, lecture seule. Procédure et pièges : ~/.claude/docs/planification_routines.md.`
- `- Pas d'agent de surveillance ni de Monitor ligne à ligne : un seul réveil à la fin. Détail : ~/.claude/docs/planification_routines.md.`
- `- Mesures de coût fixe, frontières de compaction, fonctionnement du hook de pause : ~/.claude/docs/contexte_cache.md.`
- `- Points maquette réguliers, méthode de capture avant « fini », format du rapport côte à côte : ~/.claude/docs/maquette_ui.md (+ skill captures-qt).`
- `- Vidéo/motion et modélisation 3D = Opus via architecte (jamais Sonnet pour modéliser) ; vidéos d'applis Éclat = Sonnet medium. Détail : ~/.claude/docs/video_motion.md.`
- `- Codex/OpenAI arrêté : aucun appel. Illustrations : GPT seulement à la demande de Nolann ; avant de dessiner moi-même, proposer GPT en une ligne. Détail : ~/.claude/docs/codex_illustrations.md.`

## 3. Taille estimée

Avant : 25,9 Ko (~7,5-8 k tokens relus à chaque message). Après : ~14,5-15 Ko (~4,5 k tokens). Gain ~3 k tokens/message.

## 4. Règles dures à garder ENTIÈRES (risque si résumées)

- Délégation OBLIGATOIRE + « avant chaque Read/Edit/Write : un agent peut-il le faire ? » + relire la diff : résumée, Sonnet retombe dans l'exécution directe (cause première du coût).
- Déclencheurs d'architecte 1-6 + « le plan n'exige que des commandes lançables, avec repli » : sans la liste, Sonnet attend de « se sentir bloqué » (constaté).
- File des demandes (+ restructurer au-delà de ~6 points) : règle récente, vécue ; un résumé perd « avant d'être traitée » et « jamais lâcher pour la dernière phrase ».
- Doute = pop-up (AskUserQuestion, recommandation en premier) : court, à garder mot pour mot.
- État des lieux, 1re ligne obligatoire « État des lieux : … » : la phrase « pas de ligne = faute » est ce qui la fait tenir.
- SUIVI.md réécrit avant chaque compte rendu : la « règle dure » doit rester en gras, sinon oubli avant la pause d'1 h.
- Interdit de contourner : garder la liste des cas (exception, cas spécial, test contre doc) ; un résumé ouvre la porte au contournement.
- Thème sombre : garder « fond ET texte, jamais de couleur par défaut, vérifier en sombre » ; la recette Qt peut aller dans maquette_ui.md.
- Maquette : barrière « maquette = Opus ultracode » + « tout écart = décision de Nolann » + capture côte à côte avant « fini ».
- Jamais changer de conversation en plein chantier ; jamais kill de tous les python.exe.

## 5. Doutes

- Plafond 100 k caractères/agent et « 5 min » : chiffres, mais ce sont des règles d'action ; je les garde (sans le calcul).
- Seuil ~30 k de délégation : sans lui, l'exception « geste d'une ligne » devient floue ; je garde la règle, sors les mesures.
- Mesures « Sonnet medium = high », « Sonnet = Opus, 45-50 % moins cher » : servent à justifier le choix ; les sortir risque qu'une session repropose high/Opus. Je garderais une demi-ligne « (mesuré, voir docs) ».
- Contradiction à trancher par Nolann : « Recherche web → toujours chercheur, jamais en direct » vs « chercheur indisponible → WebSearch en direct ». Proposé : « toujours chercheur ; s'il est indisponible, en direct ».
- « CLAUDE.md ≈ 8 k » dans Coût fixe : à remesurer après ménage.
- Planification/routines : utilisé rarement mais l'erreur coûte (routine qui bloque) ; la ligne de renvoi garde la décision, ok.
