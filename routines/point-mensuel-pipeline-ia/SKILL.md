---
name: point-mensuel-pipeline-ia
description: Chaque 1er du mois : veille sur les nouveautés Claude et liste des règles de la pipeline à alléger
---

Tu travailles pour Nolann (francophone). Mission : point mensuel sur sa pipeline Claude Code (sans Codex depuis le 22/10/2026) pour vérifier qu'elle ne bride pas les nouveaux modèles. Reste léger et peu coûteux ; ne modifie AUCUNE règle, skill ou agent, ne lance AUCUN banc de test.

1. Lis C:\pipeline\docs\point-mensuel.md (check-list et journal) et C:\pipeline\docs\registre-config.md (le POURQUOI de chaque skill, agent, hook et règle).
2. Lance `powershell -NoProfile -ExecutionPolicy Bypass -File C:\pipeline\outils\inventaire.ps1` (sans -Update) : liste ce qui a été ajouté, modifié ou supprimé dans ~/.claude depuis le dernier relevé (Nolann modifie aussi sa config depuis d'autres conversations et comptes). Pour chaque changement, lis le fichier concerné (lecteur si 3 fichiers ou plus) et dis ce qui a changé et si ça contredit le registre.
3. Lance l'agent `chercheur` (un seul appel) : nouveautés du dernier mois sur Claude Code (notes de version), les modèles Claude (nouveaux modèles, prix, effort, contexte) et les limites/quotas de l'abonnement Max. Il rend URL + résumé court.
4. Compare avec les règles de CLAUDE.md et le registre : lesquelles sont peut-être devenues inutiles ou contre-productives ? Pour chacune : la règle, pourquoi elle est suspecte, le test simple pour la confirmer (sans le lancer).
5. Modifications autorisées : ajouter UNE ligne au journal de point-mensuel.md, ajouter au registre les éléments nouveaux (ligne « à compléter » si le pourquoi est inconnu), puis relancer inventaire.ps1 avec -Update pour enregistrer le relevé.
6. Rapport court à Nolann (20 lignes max) : changements de config détectés, nouveautés, règles à tester ou alléger, s'il faut relancer le banc ENH-004, questions sur les éléments au pourquoi inconnu. Termine par « Mode conseillé : medium ».