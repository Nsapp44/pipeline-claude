---
name: codex-gpt
description: Dialoguer directement avec GPT via le CLI Codex (compte ChatGPT de Nolann) pour générer des images / planches de plans, obtenir un avis technique ou de modélisation CAO. À utiliser dès qu'un projet a besoin de visuels de design, de vues orthographiques cotées, ou d'un second avis de modélisation. Contient aussi (EXECUTANT.md) les règles pour utiliser Codex comme exécutant / relecteur / chercheur (rôles cx.sh, quota, partage 60/40). Complète prompts-chatgpt-images (rédaction des prompts).
---

# Parler à GPT par le CLI Codex

**Codex comme exécutant, relecteur ou chercheur (code, revue, quota, rôles `cx.sh`) : lire d'abord `EXECUTANT.md` (même dossier).** Le reste de ce fichier = dialogue image / CAO.

Nolann a un abonnement ChatGPT ; `codex` y est connecté (vérifié le 10/10/2026, codex-cli 0.162.1, « Logged in using ChatGPT »).
**Jamais d'identifiants dans le chat ni dans un fichier** : on utilise seulement l'outil déjà connecté.

## Règle de validation (Nolann, 10/10)
**GPT peut se tromper ; je peux me tromper en le jugeant.** Après avoir obtenu ce qu'il me faut, **je montre les images / résultats
à Nolann** (SendUserFile) avec mes remarques (bon / faux point par point) et j'attends sa confirmation avant de
modéliser ou de figer une décision. Pas seulement à la fin : de temps en temps, dès qu'un résultat sert de base.

## Limite de la version actuelle (mesuré le 10/10/2026, Windows)
Codex impose une **sandbox en lecture seule** et bloque les commandes shell du modèle (« rejected: blocked by policy »),
quelles que soient les options (`-s workspace-write`, `--add-dir`, `-c sandbox_permissions=…`). **Il ne peut donc ni lire ni
écrire dans le dossier du projet.** Il ne voit que le texte de la consigne (stdin) et les images `-i`.
Seul contournement = `--dangerously-bypass-approvals-and-sandbox` (accès total au PC) : **jamais sans accord explicite de Nolann.**

## Solution : le script injecte le contexte (zéro token de ma conversation)
Dans le dossier du projet, créer `_codex\` avec :
- `base_fiche.txt` : fiche des cotes faisant foi + interdits + style (en anglais), réutilisée à CHAQUE appel ;
- `appel.ps1` (script à écrire dans le projet sur le modèle de `outils/cx.sh`) : concatène fiche + `.md` choisis + tâche, joint
  les images, lance Codex, affiche la réponse en UTF-8 et copie le PNG généré dans `ref\gpt_<Nom>.png`.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File _codex\appel.ps1 -Tache _codex\tache_x.txt -Docs DESIGN.md,SUIVI.md `
   -Images ref\gpt_planche_ortho_v1.png,Schemas\v4.png -Nom planche2 [-Image]
```
- `-Docs` : fichiers du projet à envoyer en entier (lus par le script, **je ne les relis pas** ; ne pas en mettre plus que nécessaire :
  chaque Ko part en tokens GPT à chaque appel). `-Image` : demande `image_gen` et récupère le PNG.
- `-ExecutionPolicy Bypass` (portée du processus seulement) est nécessaire : la politique PowerShell bloque `appel.ps1`. `-Docs`/`-Images` : listes séparées par des virgules (le script les découpe).
- Lancer en **arrière-plan** (`run_in_background`) : 2 à 6 min pour une image. Ne pas surveiller, attendre la notification.
- Quand une information du projet change (cotes…), **mettre à jour `base_fiche.txt`** : c'est la mémoire de GPT.
- Les cotes écrites en texte **priment sur les images** (un ancien PNG à 110 de profondeur lui a fait lire 110 au lieu de 114).

## Choix du modèle (Nolann, 10/10/2026)
« Le 5.6 est un peu faible. » `appel.ps1 -Modele` : **`gpt-6.1-sol` par défaut (Nolann 28/10 : on n'utilise pas gpt-6-sol)** (testé, répond), `gpt-6-astra` selon le besoin
(Nolann teste lui-même), `gpt-5.6-*` seulement pour du code ou des questions simples. Liste : `~/.codex/models_cache.json`.
Pas d'accès complet au PC (pas de bypass) : le contexte passe uniquement par le script (`-Docs`, fiche, `-Images`) ; si GPT
manque d'un document, c'est à moi de choisir lequel lui joindre.

## Détails de l'appel
- `codex.cmd` (pas `codex`, ni `npm` : PowerShell bloque les `.ps1`) ; PATH à compléter : `$env:Path += ";C:\Program Files\nodejs;$env:APPDATA\npm"`.
- Consigne par stdin (`-`) ; `-o fichier.txt` écrit sa dernière réponse ; relire avec `Get-Content -Encoding UTF8` (sinon mojibake).
- Images : outil `image_gen` ; PNG dans `~/.codex/generated_images/<session>/exec-*.png` ; **je le copie moi-même** (le script le fait).
- Coût mesuré : ~15 à 30 k tokens GPT par appel (fiche + docs + image). Texte seul = beaucoup moins qu'une image.

## Bien lui parler (il faut des prompts techniques)
- Un prompt = **un seul livrable** (une vue, une question). Sinon il bâcle.
- Base commune en anglais (dans `base_fiche.txt`) : produit, cotes en mm, matière/fabrication, **interdits**, style (orthographique,
  fond blanc, cotes lisibles).
- Corrections : « Edit the attached image (image 1 = your previous sheet). Keep … Apply ONLY: 1) … 2) … » — numéroter,
  demander de **garder tout le reste**. Il a besoin de corrections précises par vue (ex. quelle couture, quelle cote lue de travers).
- Il ignore des consignes ou lit mal une cote : **vérifier point par point** chaque image avant de la juger bonne, dire à Nolann ce qui manque.
- **Économie** : plan texte d'abord (« liste les vues et cotes que tu vas dessiner, signale les manques »), corriger le plan, puis UNE image,
  puis corrections ciblées (jamais refaire tout de zéro). S'il y a une contradiction entre fiche et référence visuelle, la
  trancher avec Nolann AVANT l'image.
- Il pose lui-même ses réserves (ex. « disposition des couvercles fausse ») : les lire dans sa réponse.

## Pour la modélisation CAO
GPT est très fort sur certains points (géométrie, API, méthode) : **lui poser les questions de modélisation difficiles**
(ordre des fonctions, congés qui échouent, épaisseurs aux angles, stratégie d'esquisse) en collant l'extrait de code dans
`-Docs`/la tâche, avant d'insister seul. Confronter sa réponse à `architecte` / aux vérifications (volumes, sonde.py) : ne rien appliquer sans contrôle.

## Journal
Noter dans le `DESIGN.md` du projet : prompt envoyé (nom du fichier `_codex\tache_*.txt`), image obtenue (chemin), verdict de Nolann.

## Dialogue de modélisation avec GPT (appris le 10/10/2026, Di'lib'kette ; Nolann : « tu apprends à discuter avec lui »)
Nolann veut des **allers-retours**, pas une question isolée : GPT a des idées de modélisation que je n'ai pas, moi je relis et je teste.
1. **Lui donner de quoi répondre** : `-Docs` = mon script de construction en entier + `swlib_api.txt` (signatures de ma bibliothèque,
   `grep "public .*("`) ; `-Images` = la référence **et** mon rendu actuel (g_avant / g_iso). Il ne lit pas mes fichiers : tout passe par le script.
2. **Dire ce qui ne va pas, avec les mots de Nolann** (« presque que concave, 1 cm de plat au milieu »), mon état actuel (rayons posés,
   ce qui échoue) et mes contraintes dures (épaisseurs, fenêtre, fente…). Il chiffre alors honnêtement : il a refusé R35–R40 en
   montrant que l'ouverture tombait à 46 mm au lieu de ≥ 60.
3. **Demander 4 livrables** : (A) cotes lues sur la référence, (B) méthode dans l'ordre + pourquoi robuste + alternatives rejetées,
   (C) **code C# compilable** dans mon style (`sw.*`, mm) avec les prédicats de sélection d'arêtes, (D) mesures de vérification.
   Lui demander explicitement **quelle fonction de l'API utiliser** (ex. `InsertCombineFeature`, loft avec guides, congé rayon variable).
4. **Relire, ne pas coller** : compiler, construire par étapes, mesurer les épaisseurs (Mesure.exe), regarder la capture ; si ça échoue,
   lui renvoyer **l'erreur exacte et les coordonnées** (« fillet failed sur l'arête X, Y, Z ») et redemander une variante. Plusieurs tours.
5. **Il ne peut pas tout voir** : il le dit (« pas validé dans SolidWorks », « rayons 3D non identifiables ») ; ses réserves sont utiles
   (ex. incompatibilité de cotes qu'il a trouvée sur la sortie de vis). Les relever et les trancher avec Nolann.
6. Deux appels en parallèle sont possibles (rayons chiffrés + script) ; lancer avec `run_in_background` **sans `&`** dans la commande
   (sinon le processus s'arrête avec le shell et la réponse reste vide).
7. À la fin d'un chantier, noter ici ce qui a marché (méthode retenue, pièges de l'API) pour la fois suivante.
8. **`base_fiche.txt` = source unique des décisions** : la mettre à jour après chaque décision de Nolann (et garder l'ancienne en `_avant`).
   Quand GPT signale une « contradiction » ou refuse de coder (Astra, 10/10 : Y=102 vs 80, joues 4 vs 10), **comparer d'abord fiche et code** :
   la fiche périmée est la cause habituelle. Lui répondre par la décision (« voici ce qui est retenu »), comme dans une revue de conception,
   en précisant ce qui est **hors périmètre** (ne pas rouvrir), et lui dire « si une valeur manque, pose une hypothèse en une ligne et continue ».
9. Dire à GPT **ce que ma bibliothèque sait faire** (congé uniforme seulement, pas de loft…) pour qu'il choisisse une méthode réalisable.
10. **Quota ChatGPT** : l'appel échoue avec « usage limit … try again at HH:MM » (10/10, après ~5 appels Astra en 1 h) et écrit un fichier réponse vide.
   Lire la fin du `.output` avant de croire à un bug de chemin ; ne pas relancer en boucle : avancer seul et reposer la question à l'heure indiquée.
   Les chemins de `-Docs/-Images/-Tache` sont relatifs à la racine du projet (pas à `_codex`).
