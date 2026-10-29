# Consignes générales de Nolann (toutes les sessions Claude Code)

(Détails, mesures et textes complets sortis le 24/10/2026 : `~/.claude/docs/` ; sauvegarde intégrale : `docs/CLAUDE_avant_menage_2026-10-24.md`.)

## Économie de tokens et modes d'effort

- **Me dire quel mode d'effort il faut** quand la nature du travail change (une ligne « mode conseillé : … »). Je change le mode moi-même.
  - **medium** : par défaut partout. **élevé (high)** : seulement si je le demande (mesuré, voir docs : Sonnet medium = high en qualité).
  - **ultra (ultracode)** : seulement pour les problèmes extrêmement complexes (architecture, gros chantiers multi-fichiers avec relecture croisée). Repasser à un mode plus léger dès que c'est fini, et me le dire. **Au début de chaque nouveau projet, me rappeler de passer en ultracode pour l'architecture**, puis de redescendre en élevé dès qu'elle est posée.
- **Modèle principal : Sonnet 5.5 par défaut** (mesuré, voir docs : même note qu'Opus, ~45-50 % moins cher). Opus seulement dans une conversation dédiée à un gros travail d'architecture ou à un problème très dur (choisi au démarrage, jamais en cours de conversation). Changer d'effort ou de modèle en cours de conversation recrée tout le cache : seulement si la conversation est courte, sinon nouvelle conversation avec note de passation.
  - **Advisor (rétabli le 26/10/2026, compte Max)** : si l'outil `advisor` est dans la liste de la session, **appel OBLIGATOIRE (durci le 29/10/2026 : aucun appel trouvé dans les transcriptions des sessions)** sur un gros chantier / travail important : 1 avant de figer l'approche, 1 avant « fini » (livrable écrit/commité d'abord) ; et dès que ça galère (même erreur 2 fois). Dire « advisor : appelé » ou « non appelé, raison » dans le rapport final. Jamais à chaque étape ni pour un geste court ou une petite tâche. **S'il est absent (compte Pro/travail), pas d'advisor** : le jugement dur passe par l'agent `architecte` (Opus **medium**), consigne courte : but, fichiers, ce qui est douteux ou essayé + erreur exacte ; puis Sonnet applique son plan. `architecte` reste aussi pour les déclencheurs 1-6 ci-dessous. Pas pour « relire un diagnostic » ni pour tout un plan.
  - **Qui fait quoi** : ~80 % du temps Sonnet. Si Sonnet doute, ou si la demande est une conception floue / un changement important : **il s'arrête, écrit `SUIVI.md` (but, contexte, ce qui est connu) et me dit d'ouvrir une conversation Opus** (medium pour un changement important, ultracode pour un changement majeur d'architecture). Opus finit par un SUIVI à jour et me dit « clair, repars sur Sonnet » (nouvelle conversation).
  - **Déclencheurs d'`architecte`** (ne pas attendre de « se sentir bloqué ») : 1) un test échoue encore après 2
    corrections ; 2) une liste de « doutes sérieux » ou « non vérifié » → confier le plus important à `architecte`
    avant de rendre le rapport ; 3) des fichiers « non lus » dont dépend la conclusion → les lire avant de conclure,
    ou le dire en tête du rapport ; 4) aucun progrès sur 2 points d'étape, ou la même trace d'erreur qui revient ;
    5) contradiction test/doc, module difficile à concevoir ; 6) **design/visuel sans base** (SVG, README, écran) ou **plus de 2 allers-retours avec Nolann sur le même rendu** → `architecte` conçoit et vérifie par captures, pas de retouches Sonnet en boucle. **Son plan ne doit exiger que des commandes que la session peut lancer (pytest…), avec un repli ; si une commande est refusée, Sonnet s'adapte, il ne s'arrête pas.** Sans déclencheur, Sonnet seul.
  - **Si je suis absent** : Sonnet ne reste pas bloqué ; il appelle `architecte` (medium) sur le point précis, puis continue. High seulement si je le demande.
- **Sous-agents (quel que soit le mode)** :
  - **Haiku** (`model: "haiku"`) : très simple et mécanique (chercher, lister, relever, compter, renommer, mettre en forme, lancer une commande et rapporter sa sortie).
  - **Sonnet** (`model: "sonnet"`) : tout le reste de l'exécution (code d'une partie déjà conçue, recherches, lectures, analyses, tests, corrections ciblées). **Le modèle principal** garde conception, arbitrages, synthèse et vérification finale. Seul agent Opus autorisé : `architecte`.
  - **Quel agent** : recherche web → `chercheur` ; lecture de 3 fichiers ou plus (ou ~300 lignes) → `lecteur` ; tests/lint/captures/commandes longues → `testeur` (Haiku, ne modifie rien) ; écrire ou modifier du code décidé → `executant` (`general-purpose` et `claude` interdits dans settings.json). Relectures sur demande seulement : `chasseur-erreurs`, `securite-web`, `seo`. **Scan de sécurité complet (plugin `claude-security`, activé 29/10/2026)** : lancé depuis le fil principal, jamais par un agent, AVANT toute mise en production et sur tout livrable fini, avant de le donner à tester ; coûteux, donc pas à chaque commit. `securite-web` reste pour les relectures courantes. **Regrouper les appels d'outils indépendants dans un même tour.**
  - **Nombre** : 1 à 3 pour une tâche ordinaire ; 3 à 6 en parallèle pour un gros chantier aux morceaux indépendants ; jusqu'à 8-10 si je demande l'efficacité / la rapidité, ou en ultracode. Jamais deux agents qui écrivent dans le même fichier. Pas d'agents inutiles.
  - **Contrat de fin de délégation** : le message final d'un agent EST son livrable (jamais « j'attends les autres agents »). `executant` : diff minimal, ni renommage ni refactor hors consigne ; il s'arrête après 3 mêmes erreurs ou si son correctif en crée plus qu'il n'en règle.
  - Jamais `kill`/`taskkill` de tous les `python.exe` dans un prompt (cibler le PID).
  - Mesures (prix, bancs, cache des agents), consigne de revue de code à coller, règles d'agents du 24/10 : `~/.claude/docs/agents_delegation.md` (à lire avant de rédiger une consigne de revue ou un prompt d'agent long).
- **Geste d'une ligne** (commande courte, retouche < ~30 lignes) : pas de délégation ni d'annonce d'agent.
- **Délégation lecture / écriture / tests : OBLIGATOIRE.** Le fil principal **conçoit, tranche et vérifie** ; il ne
  fait pas l'exécution. Avant CHAQUE Read / Edit / Write / lancement de tests : « un agent peut-il le faire ? ».
  - **Écrire du code déjà conçu** (classe, fonction, bloc de tests, doc > ~30 lignes) → `executant` avec consigne
    précise (fichier, signatures, comportement, contraintes, ce qu'il rend). Le fil principal n'écrit que les petites
    retouches (< ~30 lignes) et la colle.
  - **Lire** : ≥ 3 fichiers ou ~300 lignes → `lecteur` (Haiku), sans exception.
  - **Tests / captures / commandes longues** → `testeur`, qui rapporte seulement verts / rouges + échecs utiles. `testeur` diagnostique avant de conclure « échec » et contrôle TOUT le lot.
  - **Seuil** : un agent recrée ~20-30 k de cache au démarrage ; il ne vaut le coup que s'il évite au fil principal **plus de ~30 k** de lecture ou de sortie. **Fil principal** : 1 ou 2 commandes courtes (sortie < ~50 lignes,
    coupée par head / grep), un contrôle ponctuel, un grep ciblé, un petit script de vérification. **Agent** : suite
    de tests complète, sorties longues, plusieurs captures, gros fichiers, code > ~30 lignes. Un seul agent pour un
    lot de contrôles, jamais un agent par commande.
  - **Recherche web** → toujours `chercheur` ; s'il est indisponible, WebSearch/Explore en direct, mêmes 15 recherches (une licence = 2 sources).
  - **Le fil principal relit la diff / l'extrait clé** de ce qu'un agent a écrit avant de dire « fait » (jamais
    d'aveugle) et l'écrit dans le rapport. Écrire soi-même un gros bloc qu'un agent aurait pu faire = faute.
  - Dire à Nolann, en une ligne à chaque lancement, quel agent et pour quoi (« lecteur : lit X »).
  - Navigateur (captures, pages longues) dans un agent dès plus de 2-3 captures.
- **Un agent n'attend jamais plus de 5 min** (son cache dure 5 min) : il lance la commande longue en arrière-plan, rend la main avec ce qu'il a lancé et où lire le résultat ; un nouvel agent l'analyse. **Une consigne = un seul livrable** ; pas de boucle « je construis, je capture, je regarde » dans l'agent qui construit (vérification visuelle à part) ; lire des extraits plutôt que des fichiers entiers ; **vers 30 appels d'outils, faire le point et rendre ce qu'on a**. **Plafond de lecture par agent : ~100 000 caractères (≈ 30 k tokens)** de résultats d'outils ; au-delà, scinder en plusieurs `lecteur` en parallèle sur des sous-ensembles distincts, rapport ≤ 30 lignes chacun.
- **Un agent qui galère demande conseil** : même erreur 2-3 fois, approche qui ne converge pas, doute sur ce qu'on attend de lui → il s'arrête et rend la main avec le point de blocage (ce qu'il a essayé, ce qu'il propose) ; le principal tranche (`architecte` si besoin) et le relance, en passant au modèle du dessus (Haiku → Sonnet) si besoin. L'écrire dans le prompt de chaque agent.
- Planifier/relancer un travail = Planificateur de tâches Windows (script .ps1) ; rendez-vous réguliers de veille = routine Claude, lecture seule. Procédure et pièges : `~/.claude/docs/planification_routines.md`.
- Pas d'agent de surveillance ni de Monitor ligne à ligne : un seul réveil à la fin. Détail : `~/.claude/docs/planification_routines.md`.

## Contexte court (les « cache reads »)

- **File des demandes (24/10/2026)** : Nolann parle beaucoup et enchaîne les demandes ; sans plan écrit, des tâches se perdent. **Chaque nouvelle demande s'ajoute à la section « File des demandes » de `SUIVI.md`** (liste numérotée, cochée) AVANT d'être traitée ; je finis la tâche en cours, je coche, je redis la file restante en une ligne, puis la suivante. Jamais lâcher une tâche pour la dernière phrase reçue ; si la file dépasse ~6 points ou se mélange, **je m'arrête, je la restructure (regrouper, ordonner, dire ce qui est fait/en cours/à faire) et je la montre**. Nouvelle demande qui change le plan = je refais le plan, pas de coupe silencieuse. Une demande abandonnée volontairement est écrite comme telle, avec la raison. **Gros chantier ou rafale de messages : j'utilise le mode plan (EnterPlanMode) au départ et à chaque ajout important, comme avant.** **Rafale / dictée** : 1re ligne de réponse « j'ai compris : 1… 2… 3… », ajouté à la file de SUIVI.md ; doute = pop-up.

- **Doute = pop-up (24/10/2026)** : Nolann ne lit pas toujours le texte. Dès qu'une demande est floue, ambiguë ou qu'un choix lui appartient, j'utilise l'outil `AskUserQuestion` (pop-up, 2-4 options, ma recommandation en premier), jamais une question noyée dans le texte. Pendant qu'elle attend, je continue le reste de la file.
- **Nom des conversations (28/10/2026)** : format `PROJET [tâche] détail`, sans statut (ex. `SITE [SEO] titres, pied de page, h2`). Nolann travaille sur beaucoup de sujets en parallèle et doit savoir qui est qui. **1er message d'une conversation dont le titre n'a pas ce format** : pop-up `AskUserQuestion` « Comment nommer cette conversation ? » (projet + tâche, ma proposition en premier), puis `set_session_title`. Les conversations que je lance (start_session, passation, worktree) reçoivent un titre à ce format d'office.- Compaction automatique à 160 000 tokens (27/10/2026 ; plancher après compaction ~110 k, 130 k bouclait). Boucle détectée par le hook `boucle_compact.py` : **FAIRE la passation seul (skill `passation`, mode autonome), sans demander à Nolann** (décidé 27/10 : il veut que je bosse seul, sans blocage). **Fin de sujet (17/10/2026)** : dès qu'un sujet est terminé (SUIVI.md à jour) et que ma demande suivante est d'une autre nature, AVANT de commencer, dire en une ligne « nouvelle conversation conseillée, modèle/effort : X » et attendre mon choix ; un détail à corriger sur le sujet en cours se finit ici. Proposer `/compact` aux frontières naturelles, jamais en pleine implémentation, SUIVI.md à jour avant.
- **Changement de conversation pendant un chantier (assoupli le 26/10/2026)** : pas de `/clear` ni de changement de modèle en plein travail. Mais **un lot fini = point de passation possible** si les 3 sont réunis : 1) lot terminé ; 2) `SUIVI.md` réécrit propre (décisions en vigueur, **liste des OK validés**, le « pourquoi » des décisions orales, prochain pas) ; 3) **script de non-régression vert** (rebuild + contrôles + comparaison aux références validées ; à créer si le chantier a des rendus à ne pas casser, et à relancer dans la nouvelle conversation). Alors je dis « point de passation propre, nouvelle conversation conseillée » ; Nolann choisit. Script rouge ou SUIVI.md incomplet = on reste. **Si Nolann dit qu'il s'absente** (« fais tout seul, je reviens demain ») : ne PAS demander de changer de conversation (il ne répondra pas) ; compaction et SUIVI.md suffisent. Contexte énorme (conversations de plusieurs millions de tokens) : le point de passation est le moyen normal de repartir léger, pas une exception. Les détails de code ne sont pas dans SUIVI.md : on les relit à la demande.
- Coût fixe : garder ce fichier court, pas de serveur MCP sans besoin ; mon accord avant de retirer/désactiver un MCP ou de toucher aux réglages. Mesures, frontières de compaction, hook de pause : `~/.claude/docs/contexte_cache.md`.
- Pause de plus d'1 h = cache perdu ; si je dis « pause », écrire SUIVI.md avant que je parte.
- **`SUIVI.md` = ÉTAT COURANT seulement** (viser ≤ ~5 Ko, jamais d'accumulation ; **lu UNE fois** au démarrage, après compaction ou grosse pause, jamais entre deux messages : il est déjà dans le contexte ; hook `suivi_taille.py` alerte > 8 Ko) : décisions en vigueur, état actuel, **« Ce qui n'a pas marché et pourquoi »**, **« Prochain pas exact »** (section vide = « rien pour l'instant », on ne la supprime pas). **RÉÉCRIT (pas complété)** à chaque étape ou décision, sans que je le demande. **Règle dure : AVANT chaque compte rendu à Nolann et à la fin de chaque étape terminée, SUIVI.md est réécrit propre (état, prochain pas exact) ; jamais de réponse avant.** Ce qui est fini et son détail vont dans `docs/` (archives, journal, spec) avec un renvoi d'une ligne. Même règle dans chaque projet, avec la règle de docs techniques du projet. **Après compaction ou pause, relire SUIVI.md d'abord.** **Un SUIVI par chantier** (SEO, paiement multi-colis, boutique…), chargé seulement par la session de ce chantier ; chantier fini ou en pause = fiche `docs/chantiers/<chantier>.md` (modèle : `~/.claude/docs/modele_fiche_chantier.md`) pour le reprendre plus tard sans traîner l'historique. **Zéro perte à l'allègement (28/10/2026 ; test : 1 info introuvable sur 10 sur un SUIVI sur-mesure)** : on DÉPLACE sans réécrire (copie `.bak` avant, l'archive garde le texte d'origine) ; le SUIVI court garde les valeurs exactes, les listes ordonnées et un **index des archives** (« sujet → fichier, section ») ; contrôle avant de conclure : 10 questions tirées de l'ancien SUIVI, toutes retrouvables dans court + archives. **Note de passation lue par une nouvelle session = supprimée** une fois reprise (résultats durables dans `docs/`).
- **Contexte léger / docs d'abord** : lire la doc du projet (README, CLAUDE.md, docs/) avant le code ; chercher (Grep/Glob) avant de lire ; ne lire que les parties utiles, couper les sorties longues (head / tail / grep). **Le fil principal ne lit que** : le fichier qu'il va modifier juste après (offset/limit), ou un extrait trouvé par Grep. Code exact d'un gros fichier à recopier ? Le copier par commande (Copy-Item). **Avant chaque lot de lectures, se demander « combien de fichiers ? »** : 3 ou plus = un agent `lecteur`.
- CLAUDE.md global : 20-25 Ko maxi (décidé 24/10, règles dures gardées entières) ; on garde toujours UN fichier « avant ménage » dans `docs/` (jamais utilisé, juste au cas où). CLAUDE.md d'un projet : ~15 Ko maxi, seulement ce qui sert à chaque message ; le détail va dans `docs/`. Le hook `claude_md_taille.py` signale un fichier trop gros ; je lance alors le skill `menage-claude-md` à la fin de la tâche.
- **Interdit de contourner** : si, pour faire passer un test, tu dois ajouter une exception ou un cas spécial, ou si
  deux tests (ou un test et la doc) se contredisent → ne pas coder le contournement. Laisser le test rouge, appeler
  `architecte` (medium, consigne courte : la contradiction exacte, les fichiers) ou me demander de trancher. Jamais
  « douteux à signaler » après coup (Sonnet contourne 3 fois sur 3, Opus refuse).

## État des lieux avant de se lancer

- **Avant chaque tâche, état des lieux de ce qui existe déjà** : code et historique git du projet, outils et bibliothèques (GitHub, PyPI…), recherche web (méthodes, normes, exemples). But : **s'en inspirer, ou l'utiliser / le copier** plutôt que tout refaire. Vérifier la licence avant de copier du code (et la citer) : me dire si elle permet un usage commercial ; absente ou douteuse → ne pas copier, me prévenir. Dire en une ligne ce qui a été trouvé et ce qu'on reprend. **Proportionné** : petite modif → un coup d'œil au code concerné, sans agent ni recherche web ; nouvelle fonction → recherche ciblée (un agent Sonnet au plus) ; gros chantier ou sujet inconnu → vraie recherche (web, GitHub, git).
- **Rappel de Nolann (24/10/2026) : cet état des lieux se perdait.** Toute question ou demande qui crée du NOUVEAU (outil, fonction, méthode, skill, vidéo, mise en page, « est-ce que ça existe ? ») démarre par : 1) `git log`/`grep` du dépôt et des projets voisins ; 2) **`chercheur` (15 recherches mini, GitHub et alternatives)**, lancé en parallèle du reste. **La 1re ligne de ma réponse dit le résultat** : « État des lieux : trouvé X (licence Y), on reprend / rien de probant après N recherches ». Pas de ligne = je l'ai sautée = faute. Seules vraies exceptions : correction d'une ligne, question pure d'explication, suite directe d'un état des lieux déjà fait dans la conversation.

## Applis avec une interface : maquette d'abord, points visuels ensuite

- **Ne pas coder à vue.** Au début d'une appli (ou d'un nouvel écran important) : **architecture + mini maquette**
  avant le code (skills de design, Artifact avec écrans, ou conversation Opus avec captures), validée par moi. Une
  référence (« comme l'appli X ») ne remplace pas la maquette.
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
- **Skills et agents (27/10/2026)** : un skill que seul le fil principal charge ne sert presque jamais, car le travail part chez les agents (sans outil Skill). À chaque skill créé : se demander quel agent doit l'avoir et l'ajouter à sa ligne `skills:` (frontmatter, fichier en LF, jamais CRLF) dans la foulée.
- **Code d'interface (page, CSS, composant, texte visible) → agent `executant-ui`** (skills de design préchargés), jamais `executant`. Le fil principal charge `web-design-guidelines` avant toute retouche d'écran, même petite (27/10/2026).
- **Lot d'interface** : lire `web-design-guidelines` + `design:design-critique`, recopier la checklist dans le brief `executant`/`architecte` (qui n'a pas l'outil Skill), et je regarde les captures avant « fait ».
- **Thème sombre de Windows (toutes les applis)** : il casse les interfaces qui se fient aux couleurs du système.
  Toujours fixer soi-même fond **et** texte (Qt : style Fusion + `QPalette` claire explicite + QSS avec `background`
  et `color` sur chaque widget stylé), jamais de couleur « par défaut », et **vérifier chaque nouvel écran, dialogue ou
  popup avec Windows en mode sombre** avant de livrer.
- Points maquette réguliers, méthode de capture avant « fini », format du rapport côte à côte : `~/.claude/docs/maquette_ui.md` (+ skill `captures-qt`).
- **Mascotte commune à la suite de logiciels** : même mascotte dans chaque logiciel ; règles dans `~/.claude/docs/mascotte.md` (à lire avant d'y toucher).

## Vidéo / motion / modélisation

- Vidéo/motion et modélisation 3D = Opus via `architecte` (jamais Sonnet pour modéliser) ; vidéos d'applis = Sonnet medium. Détail : `~/.claude/docs/video_motion.md`.

## Produit physique (CAO / SolidWorks)

Concevoir avant de modéliser (schéma 2D coté → prompts d'images → relecture technique → modélisation par étapes) : je le propose moi-même à chaque étape. Workflow complet : `~/.claude/docs/produit_physique_cao.md`.

## Codex / OpenAI : seulement à la demande

- Dans cette variante, Claude travaille seul ; le skill `codex-gpt` reste installé mais n'est jamais lancé de lui-même. Illustrations : GPT (modèle `gpt-6.1-sol`, jamais `gpt-6-sol`) seulement quand je le demande ; avant de dessiner moi-même, proposer GPT en une ligne. Pour le code ou l'analyse déléguée à GPT : uniquement sur ma demande, règles dans `skills/codex-gpt/EXECUTANT.md`.

## Skills

- **Nouveau projet ou changement de sujet** : utiliser les skills installés qui correspondent au travail (ex. écrans Qt : `qt-ui-design` ; textes : `design:ux-copy` ; relecture : `design:design-critique`, `design:accessibility-review`). Un travail qui se répète : **proposer de créer un skill**.
- **Créer/modifier un skill, agent, hook ou règle** : ajouter une ligne (pourquoi, date, mesure) à `docs/registre-config.md`, jamais le pourquoi dans le skill ou ce fichier. « Mis à jour sur un autre compte » : `outils/inventaire.ps1 -Extra <dossier>`.
