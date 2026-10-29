# Registre de la configuration (le POURQUOI de chaque élément)

But : quand le point mensuel (ou un « j'ai mis à jour ») relit skills, agents et règles, ce fichier donne le contexte : pourquoi ça existe, ce qui a été mesuré, quoi vérifier. À tenir à jour à chaque ajout. Ce qui a changé est détecté par `outils/inventaire.ps1` ; ce fichier explique.

Travail sur plusieurs comptes / conversations : l'inventaire ne voit que les dossiers qu'on lui donne (`-Extra "D:\autre\.claude"`). Pour un autre compte, Nolann dit « mis à jour sur le compte X, dossier Y ».

| Élément | Pourquoi il existe | Mesuré / daté | À vérifier au point |
|---|---|---|---|
| Agents `lecteur`, `chercheur`, `testeur` (Haiku/Sonnet) | Garder le fil principal court : lecture, web et tests en agents moins chers | cache d'un agent ≈ 20-30 k, rentable si évite > 30 k | seuils encore justes ? |
| Agent `executant` | Écrire du code déjà conçu sans charger le fil principal ; `general-purpose` et `claude` interdits (5× plus chers) | 12/10/2026 | idem |
| Agent `architecte` (Opus medium) | Jugement dur sans advisor sur ce compte ; déclencheurs précis (test qui échoue après 2 corrections, contradictions) | ~0,08 $ l'appel | compte avec advisor maintenant ? |
| Agents `chasseur-erreurs`, `securite-web`, `seo` | Relectures sur demande, jamais automatiques | — | encore utilisés ? |
| Skill `codex-gpt` (+ `cx.sh`) | Codex = exécutant, partage visé 30 % Claude / 70 % Codex ; pipeline par défaut Codex implémente + 1 vérification Sonnet | ENH-004, 17/10/2026 : 0,53 $, 7 échecs | relancer le banc ; quotas OpenAI |
| Skill `publier-repo` | Scan anti-fuite (noms privés, secrets) avant tout push public | 17/10/2026 | liste `mots-interdits.txt` à jour |
| Skill `creer-repo-public` | Produire de beaux dépôts publics (README, docs, CLAUDE.md, captures fictives) | 17/10/2026 | exemples de référence toujours bons |
| Skills `qt-ui-design`, `captures-qt`, `maquette-canevas` | Interfaces : maquette validée avant le code, code fidèle à la maquette, captures hors écran + contrôle mode sombre Windows. | 10-11/10/2026 | — |
| Skill `installateur-msi` | Livrer une appli Windows (Python/PyInstaller) avec un vrai installateur .msi WiX 5 (écrans, raccourcis, « Lancer l'appli ») ; évite de réécrire le .wxs de zéro | 11/10/2026 | chemins de référence toujours valides ? WiX 5.0.2 |
| Skill `prompts-chatgpt-images` | Produit physique : écrire des prompts d'images (ChatGPT / Nano Banana) lisibles comme des plans, pour modéliser en CAO ; né d’un projet de produit physique. Un seul prompt (coupe de profil) au premier envoi | 14/10/2026 | utile tant que GPT génère les visuels ; voir `codex-gpt` |
| Skill `web-design-guidelines` | Installé tel quel de Vercel (auteur vercel, v1.0.0) : revue d'une interface web contre les Web Interface Guidelines (accessibilité, UX) | 10/10/2026 | encore appelé ? sinon supprimer |
| Skill `menage-claude-md` | Ramener un CLAUDE.md de PROJET sous ~15 Ko sans rien perdre (détail déplacé dans `docs/`), lancé quand le hook `claude_md_taille` le signale. Exclut le CLAUDE.md global (décision de Nolann 12/10) | 12/10/2026 | seuil 15 Ko encore juste |
| Dossier `synced` | Skills synchronisés par l'appli Claude (`built-in-browser`, `chrome-browser`, ...), licence propriétaire : ne pas les modifier, ils sont recréés | — | rien à faire |
| Hooks `pause_longue`, `claude_md_taille`, `conso_5h`, `protege_fichiers` | Pause > 1 h = cache perdu (bloque le message de reprise) ; CLAUDE.md trop gros ; jauge 5 h ; protection de fichiers | 12/10/2026 | encore utiles / bloquants ? |
| Règles CLAUDE.md global : Sonnet par défaut, effort medium, délégation obligatoire | Coût mesuré : Sonnet = Opus en note, ~45-50 % moins cher | 12-17/10/2026 | un nouveau modèle change-t-il la donne ? |
| Barrière « maquette = Opus ultracode » (CLAUDE.md global, section interfaces) | Une session Sonnet a fait/évité une maquette sans appliquer la règle (le « ou » laissait le choix). Barrière avant + filet de retour Opus. Changement léger = Sonnet + relecture `architecte` des captures, rapport avant/après + verdict obligatoire | 17/10/2026 | encore des maquettes faites sur Sonnet ? |
| Règle « fin de sujet = proposer une nouvelle conversation » (CLAUDE.md global, contexte court) | Cas vécu 17/10 (conv Bureau entreprise) : proposition faite trop tard, après compaction. Sujet lié = nouvelle conv quand même, SUIVI.md porte le contexte | 17/10/2026 | proposée à temps ? |
| Rôle `cx.sh visuel` + refus d'`executant` sur consigne visuelle (cx.sh, EXECUTANT.md, CLAUDE.md global) | v5b (maquette chats) faite par `executant` sol low : éléments qui glissent ; `architecte` Codex est en lecture seule. Visuel = astra high avec écriture, mais sur demande seulement : le visuel brûle le quota Codex, Opus ultracode est moins cher (Nolann 18/10) | 18/10/2026 | encore des tâches visuelles passées en `executant` (CX_FORCE) ? |
| Routine : `point-mensuel-pipeline-ia` | Rendez-vous réguliers de veille (exception à « Planificateur Windows ») | 17/10/2026 | — |

## Journal des changements décidés
- 17/10/2026 : création du registre et de l'inventaire (`outils/inventaire.ps1`, relevé `docs/inventaire.json`).
- 17/10/2026 : « pourquoi » complété pour les skills Qt, installateur-msi, prompts-chatgpt-images, web-design-guidelines, menage-claude-md, synced (déduit de leurs SKILL.md et dates ; le choix de `web-design-guidelines` n'est pas documenté).
- 20/10 : règle « Routine Claude » ajoutée (CLAUDE.md global + AGENTS.md du dépôt public) : run = session locale dans le dossier de création, pas de réglage dossier/autorisations, pas de mode Auto sans accord.

| 22/10/2026 | Codex/OpenAI retiré de la pipeline (CLAUDE.md global : section GPT/Codex remplacée par une note de 5 lignes ; routine point-mensuel nettoyée) | Abonnement OpenAI arrêté, passage à Claude Max | Ancienne version : tag git avec-codex-2026-10-22 (~/.claude), branche pipeline-claude-seul = référence. Skills codex-gpt etc. laissés installés. |
| 22/10/2026 | CLAUDE.md : déclencheur 6 d'architecte (design sans base ou plus de 2 allers-retours) ; skill verif-responsive-web ajouté | Allers-retours Sonnet perdus ; responsive vérifié à chaque fois | À mesurer au point mensuel. |
- 24/10/2026 : `chercheur` durci (15 recherches mini, extended) ; règles File des demandes, État des lieux renforcé, Doute = pop-up, règles d agents (repli chercheur, 2 sources licence, pas de kill python.exe, testeur diagnostique), rafales, lots d interface, geste d une ligne. Origine : retours de 5 sessions de travail.
