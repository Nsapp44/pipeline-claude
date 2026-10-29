# contexte_cache.md — Sorti du CLAUDE.md le 24/10/2026

Sorti du CLAUDE.md le 24/10/2026 (texte original, mot pour mot ; sauvegarde complète : CLAUDE_avant_menage_2026-10-24.md).

- Chaque message relit **toute** la conversation. Compaction automatique à **160 000 tokens** (27/10/2026 ; 130 000 le 26/10 bouclait car le contexte repart à ~110 k après compaction ; hook `boucle_compact.py` alerte si 2 compactions en < 15 min ; hook PreCompact à 10 s) (`autoCompactWindow`
  dans `~/.claude/settings.json`). Me proposer `/clear` ou une nouvelle session (avec note de passation) quand on
  change de sujet ; ultracode seulement le temps du chantier. **Fin de sujet (17/10/2026)** : dès qu'un sujet est
  terminé (SUIVI.md à jour) et que ma demande suivante est d'une autre nature, AVANT de commencer, dire en une ligne
  « nouvelle conversation conseillée, modèle/effort : X » et attendre mon choix ; un détail à corriger sur le sujet en
  cours se finit ici. Sujet lié qui a besoin du contexte : nouvelle conversation quand même, SUIVI.md porte le contexte. **Compaction stratégique** : proposer `/compact` aux
  frontières naturelles (fin d'une recherche avant de planifier, plan écrit dans un FICHIER avant d'implémenter,
  débogage terminé, approche ratée abandonnée), jamais en pleine implémentation. Avant : SUIVI.md à jour (todos et
  raisonnement intermédiaire ne survivent pas ; CLAUDE.md, fichiers et git oui).
- **Coût fixe** : base ≈ 78 k tokens relus à chaque message (outils ≈ 39 k, MCP ≈ 21 k, CLAUDE.md ≈ 8 k, mesuré
  11/10) → garder ce fichier court, ne pas ajouter de serveur MCP sans besoin ; mon accord avant de retirer/désactiver
  un MCP ou de toucher aux réglages.
- **Jamais de changement de conversation (ni `/clear`, ni changement de modèle) pendant un dossier ou un chantier dont
  le contexte compte** (deck, rapport, rendus, décisions en route) : la reprise perd des détails = carnage. On finit
  dans la même conversation (la compaction suffit) ; nouvelle conversation seulement le dossier terminé, ou si je le
  demande.
- **Pause de plus d'1 h = cache du fil perdu** (reprise = 2 × le contexte). Le hook `hooks/pause_longue.py` bloque le
  1er message après > 1 h si contexte > 80 k (renvoyer = on continue et on paye). Si je dis « pause », écrire SUIVI.md
  avant que je parte.
- **`SUIVI.md` = ÉTAT COURANT seulement** (viser ≤ ~5 Ko, jamais d'accumulation ; relu à chaque message, 33 Ko =
  coûteux, mesuré 12/10) : décisions en vigueur, état actuel, **« Ce qui n'a pas marché et pourquoi »**, **« Prochain
  pas exact »** (section vide = « rien pour l'instant », on ne la supprime pas). **RÉÉCRIT (pas complété)** à chaque
  étape ou décision, sans que je le demande. **Règle dure : AVANT chaque compte rendu à Nolann et à la fin de chaque
  étape terminée, SUIVI.md est réécrit propre (état, prochain pas exact) ; jamais de réponse avant.** Le hook de pause
  1 h bloque le message de reprise : s'il n'est pas propre à ce moment-là, on perd le fil (vécu 12/10). Ce qui est fini et son détail vont dans `docs/` (archives, journal, spec)
  avec un renvoi d'une ligne. Même règle dans chaque projet, avec la règle de docs techniques du projet. Après
  compaction ou pause, le relire d'abord. **Note de passation lue par une nouvelle session = supprimée** une fois
  reprise (résultats durables dans `docs/`).
- Contexte léger : ne lire que les parties utiles, couper les sorties longues (head / tail / grep), faire lire les
  gros fichiers et journaux par un agent qui ne rapporte que la conclusion, rapports d'agents courts, mémoires courtes.
- **CLAUDE.md d'un projet : ~15 Ko maxi (≈ 150 lignes de 100 caractères)**, seulement ce qui sert à chaque message
  (règles et pièges, décisions à construire, où trouver le reste) ; le fait et son détail vont dans `docs/`. Un hook
  (`~/.claude/hooks/claude_md_taille.py`) signale un CLAUDE.md trop gros ; je lance alors le skill `menage-claude-md`
  (agent Opus) à la fin de la tâche.
- **Docs d'abord** : lire la doc du projet (README, CLAUDE.md, docs/, audits) avant le code. Chercher (Grep/Glob) avant
  de lire. Dès 3 fichiers, ou ~300 lignes cumulées, ou exploration de dossier → agent `lecteur` (Haiku), consigne
  précise (ce qu'on cherche, ce qu'on veut en retour : signatures, valeurs, extraits) et rapport court. **Le fil
  principal ne lit que** : le fichier qu'il va modifier juste après (partie utile, offset/limit), ou un extrait ciblé
  trouvé par Grep. Code exact d'un gros fichier à recopier ? Le copier par commande (Copy-Item), pas le lire. **Avant
  chaque lot de lectures, se demander « combien de fichiers ? »** : 3 ou plus = un agent.

- **Interdit de contourner** : si, pour faire passer un test, tu dois ajouter une exception ou un cas spécial, ou si
  deux tests (ou un test et la doc) se contredisent → ne pas coder le contournement. Laisser le test rouge, appeler
  `architecte` (medium, consigne courte : la contradiction exacte, les fichiers) ou me demander de trancher. Jamais
  « douteux à signaler » après coup (Sonnet contourne 3 fois sur 3, Opus refuse).

