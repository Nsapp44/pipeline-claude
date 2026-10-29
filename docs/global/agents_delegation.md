# agents_delegation.md — Sorti du CLAUDE.md le 24/10/2026

Sorti du CLAUDE.md le 24/10/2026 (texte original, mot pour mot ; sauvegarde complète : CLAUDE_avant_menage_2026-10-24.md).

- **Me dire quel mode d'effort il faut** quand la nature du travail change (une ligne « mode conseillé : … »). Je
  change le mode moi-même.
  - **medium** : **par défaut partout** (questions, explications, code ciblé, corrections).
  - **élevé (high)** : seulement si je le demande (mesuré : Sonnet medium = high en qualité, high ~1,6× plus cher).
  - **ultra (ultracode)** : **seulement pour les problèmes extrêmement complexes** qui ont besoin de beaucoup d'agents
    en parallèle (architecture, gros chantiers multi-fichiers avec relecture croisée). Repasser à un mode plus léger
    dès que c'est fini, et me le dire.
  - **Au début de chaque nouveau projet, me rappeler de passer en ultracode pour l'architecture**, puis me dire de
    redescendre en élevé dès qu'elle est posée.
- **Modèle principal : Sonnet 5.5 par défaut** (mesuré : même note qu'Opus, ~45-50 % moins cher). **Opus seulement
  dans une conversation dédiée** à un gros travail d'architecture ou à un problème très dur (choisi au démarrage,
  jamais en cours de conversation).
  - **Advisor (rétabli le 26/10/2026, compte Max)** : si l'outil `advisor` est dans la liste de la session, l'utiliser aux moments clés seulement : 1 appel avant de figer l'approche d'un gros chantier, 1 avant « fini » sur un travail important (livrable écrit/commité d'abord). Jamais à chaque étape ni pour un geste court. **S'il est absent (compte Pro/travail), pas d'advisor** : le jugement dur passe par l'agent `architecte` (Opus **medium**), consigne courte : but, fichiers, ce qui est douteux ou essayé + erreur exacte ; puis Sonnet applique son plan. `architecte` reste aussi pour les déclencheurs 1-6. Pas pour « relire un diagnostic » ni pour tout un plan.
  - **Qui fait quoi** : ~80 % du temps Sonnet. Si Sonnet doute, ou si la demande est une conception floue / un
    changement important : **il s'arrête, écrit `SUIVI.md` (but, contexte, ce qui est connu) et me dit d'ouvrir une
    conversation Opus** (medium pour un changement important, ultracode pour un changement majeur d'architecture).
    Opus finit par un SUIVI à jour et me dit « clair, repars sur Sonnet » (nouvelle conversation).
  - **Déclencheurs d'`architecte`** (ne pas attendre de « se sentir bloqué ») : 1) un test échoue encore après 2
    corrections ; 2) une liste de « doutes sérieux » ou « non vérifié » → confier le plus important à `architecte`
    avant de rendre le rapport ; 3) des fichiers « non lus » dont dépend la conclusion → les lire avant de conclure,
    ou le dire en tête du rapport ; 4) aucun progrès sur 2 points d'étape, ou la même trace d'erreur qui revient ;
    5) contradiction test/doc, module difficile à concevoir ; 6) **design/visuel sans base** (SVG, README, écran) ou **plus de 2 allers-retours avec Nolann sur le même rendu** → `architecte` conçoit et vérifie par captures, pas de retouches Sonnet en boucle (rare mais évite la perte de temps). **Son plan ne doit exiger que des commandes que la session
    peut lancer (pytest…), avec un repli ; si une commande est refusée, Sonnet s'adapte, il ne s'arrête pas** (bancs
    T9 16/10 : sinon 0/5). Sans déclencheur, Sonnet seul (C coûte 1,6× A sans gain mesuré).
  - **Si je suis absent** : Sonnet ne reste pas bloqué ; il appelle `architecte` (medium) sur le point précis, puis
    continue. High seulement si je le demande.
  - **Changer d'effort ou de modèle en cours de conversation recrée tout le cache** (≈ 2 × le contexte) : changer
    tant que la conversation est courte ; sinon nouvelle conversation avec note de passation (≈ 15 k).

- **Sous-agents, gradués selon la tâche**, **quel que soit le mode** : **Haiku** (`model: "haiku"`) pour le très
  simple et mécanique (chercher, lister, relever, compter, renommer, mettre en forme, lancer une commande et rapporter
  sa sortie) ; **Sonnet** (`model: "sonnet"`) pour tout le reste de l'exécution (code d'une partie déjà conçue,
  recherches, lectures et analyses, tests, corrections ciblées) ; **le modèle principal** garde conception,
  arbitrages, synthèse et vérification finale. Seul agent Opus autorisé : `architecte`.
- **Nombre d'agents** : 1 à 3 pour une tâche ordinaire (dès qu'un seuil de délégation est atteint, on lance l'agent) ;
  **3 à 6 en parallèle pour un gros chantier aux morceaux indépendants** ; **jusqu'à 8-10 si je demande l'efficacité /
  la rapidité**, ou en ultracode. Jamais deux agents qui écrivent dans le même fichier. Pas d'agents *inutiles*.
- **Choisir l'agent le plus léger** : recherche web → `chercheur` ; lecture de 3 fichiers ou plus (ou ~300 lignes) →
  `lecteur` ; tests/lint/captures/commandes longues → `testeur` (Haiku, ne modifie rien) ; écrire ou modifier du code
  décidé → `executant` (`general-purpose` et `claude` interdits dans settings.json : 5× plus chers). **Regrouper les
  appels d'outils indépendants dans un même tour.**
  **Relectures sur demande (Sonnet medium, lecture seule, jamais automatiques)** : erreurs silencieuses Python/Qt/JS →
  `chasseur-erreurs` ; avant mise en ligne web (secrets, XSS, CSP) → `securite-web` ; référencement → `seo`.
  **Consigne de revue de code** (à coller dans le prompt) : ne signaler que si sûr à plus de 80 % ; pour
  HIGH/CRITICAL, citer ligne + scénario d'échec concret + pourquoi rien ne le rattrape, sinon baisser ou abandonner ;
  « aucun constat » est valide ; pas de remarques de style ni de « pensez à X » ; format `[GRAVITÉ] chemin:ligne` /
  problème / correction, puis tableau récapitulatif.
  **Contrat de fin de délégation** : le message final d'un agent EST son livrable (jamais « j'attends les autres
  agents »). `executant` : diff minimal, ni renommage ni refactor hors consigne ; il s'arrête après 3 mêmes erreurs ou
  si son correctif en crée plus qu'il n'en règle. `lecteur` en recherche ouverte : 3 cycles au plus, chaque fichier
  noté de 0 à 1, ne rendre que ceux ≥ 0,7.
- **Règles d'agents (24/10/2026, retours des sessions)** : `chercheur` indisponible → WebSearch/Explore en direct, mêmes 15 recherches ; une licence = 2 sources. Jamais `kill`/`taskkill` de tous les `python.exe` dans un prompt (cibler le PID). `testeur` diagnostique avant de conclure « échec » (réglages par défaut, accents normalisés) et contrôle TOUT le lot (5 images sur 5). Rendu long : la commande de fin prévient aussi si le processus s'arrête avant la fin.

- **Rafale / dictée (24/10/2026)** : 1re ligne de réponse « j'ai compris : 1… 2… 3… », ajouté à la file de SUIVI.md ; doute = pop-up. **Lot d'interface** : lire `web-design-guidelines` + `design:design-critique`, recopier la checklist dans le brief `executant`/`architecte` (qui n'a pas l'outil Skill), et je regarde les captures avant « fait ».
- **Geste d'une ligne** (commande courte, retouche < ~30 lignes) : pas de délégation ni d'annonce d'agent.

- **Délégation lecture / écriture / tests : OBLIGATOIRE.** Le fil principal **conçoit, tranche et vérifie** ; il ne
  fait pas l'exécution. Avant CHAQUE Read / Edit / Write / lancement de tests : « un agent peut-il le faire ? ».
  - **Écrire du code déjà conçu** (classe, fonction, bloc de tests, doc > ~30 lignes) → `executant` avec consigne
    précise (fichier, signatures, comportement, contraintes, ce qu'il rend). Le fil principal n'écrit que les petites
    retouches (< ~30 lignes) et la colle.
  - **Lire** : ≥ 3 fichiers ou ~300 lignes → `lecteur` (Haiku), sans exception.
  - **Tests / captures / commandes longues** → `testeur`, qui rapporte seulement verts / rouges + échecs utiles.
  - **Seuil** : un agent recrée ~20-30 k de cache au démarrage (mesuré 10-22 k le 12/10 ; 30-95 k et plus pour un agent qui lit beaucoup) ; il ne vaut le coup que s'il évite au fil principal
    **plus de ~30 k** de lecture ou de sortie. **Fil principal** : 1 ou 2 commandes courtes (sortie < ~50 lignes,
    coupée par head / grep), un contrôle ponctuel, un grep ciblé, un petit script de vérification. **Agent** : suite
    de tests complète, sorties longues, plusieurs captures, gros fichiers, code > ~30 lignes. Un seul agent pour un
    lot de contrôles, jamais un agent par commande.
  - **Recherche web** → toujours `chercheur`, jamais en direct.
  - **Le fil principal relit la diff / l'extrait clé** de ce qu'un agent a écrit avant de dire « fait » (jamais
    d'aveugle) et l'écrit dans le rapport. Écrire soi-même un gros bloc qu'un agent aurait pu faire = faute.
  - Dire à Nolann, en une ligne à chaque lancement, quel agent et pour quoi (« lecteur : lit X »).
- **Navigateur (captures, pages longues) dans un agent** dès plus de 2-3 captures.

- **Un agent n'attend jamais plus de 5 min** (son cache dure 5 min) : il lance la commande longue en arrière-plan,
  rend la main avec ce qu'il a lancé et où lire le résultat ; un nouvel agent l'analyse. La durée n'est pas un critère
  d'arrêt ; ce qui coûte : une pause > 5 min et un contexte qui grossit. Donc **une consigne = un seul livrable** ;
  **pas de boucle « je construis, je capture, je regarde » dans l'agent qui construit** (vérification visuelle à part) ;
  lire des extraits plutôt que des fichiers entiers ; **vers 30 appels d'outils, faire le point et rendre ce qu'on a**.
  **Plafond de lecture par agent : ~100 000 caractères (≈ 30 k tokens) de résultats d'outils.** Au-delà, scinder en
  plusieurs `lecteur` en parallèle, chacun sur un sous-ensemble distinct (dossiers ou fichiers différents), rapport ≤ 30
  lignes chacun ; un agent qui lit 270 k caractères a écrit 160 k tokens de cache (mesuré 12/10), deux agents de moitié
  coûtent moins qu'un seul gros (chaque message relit tout son contexte), ~15 k de démarrage en plus chacun.
- **Un agent qui galère demande conseil** : même erreur 2-3 fois, approche qui ne converge pas, doute sur ce qu'on
  attend de lui → il s'arrête et rend la main avec le point de blocage (ce qu'il a essayé, ce qu'il propose) ; le
  principal tranche (`architecte` si besoin) et le relance, en passant au modèle du dessus (Haiku → Sonnet) si besoin.
  L'écrire dans le prompt de chaque agent.

