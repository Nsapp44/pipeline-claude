# planification_routines.md — Sorti du CLAUDE.md le 24/10/2026

Sorti du CLAUDE.md le 24/10/2026 (texte original, mot pour mot ; sauvegarde complète : CLAUDE_avant_menage_2026-10-24.md).

- **Planifier / relancer un travail (tests, builds, commandes) = Planificateur de tâches Windows via PowerShell**
  (`schtasks` / `Register-ScheduledTask`, script `.ps1` plutôt que commande inline), car les routines de l'appli
  bloquent sur les autorisations. **Exception (décidée 17/10/2026) : les rendez-vous réguliers de veille ou de point
  (mensuel, hebdo : point Éclat, point mensuel pipeline) = routine Claude**, visible dans « Scheduled » ; lecture et
  rapport seulement, aucune action risquée. Pas de skip des permissions ; dire à Nolann ce que la tâche lance.
  **Routine Claude (vérifié 20/10)** : chaque run = une vraie session locale, dans le dossier du projet où la routine a été créée
  (le créer depuis la conversation du projet concerné), listée dans « Tâches planifiées », archivable ; pas de réglage de dossier ni
  d'autorisations dans l'outil ; jamais créée en mode Auto sans l'accord de Nolann.
- **Pas d'agent de surveillance** : attendre les notifications de fin, ne jamais faire tourner un agent ou une boucle
  qui vérifie « c'est fini ? ». Point d'avancement = une commande courte quand on me le demande ; longue attente
  (plusieurs heures) = script ou tâche planifiée Windows, sans tokens. **Pas de Monitor qui notifie à chaque ligne de
  progression** : **un seul réveil à la fin** (commande en arrière-plan qui attend la fin, puis affiche la queue du
  log). Monitor seulement pour les erreurs et la fin ; ne rien écrire entre deux réveils.

