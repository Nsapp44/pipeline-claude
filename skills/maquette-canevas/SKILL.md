---
name: maquette-canevas
description: Faire, vérifier ou publier une maquette d'écrans en planches interactives sur un canevas claude.ai (artefact de type Design), avant de coder une interface. À utiliser au début de toute appli ou de tout nouvel écran important, et pour les « points maquette ».
---

# Maquette d'écrans sur un canevas claude.ai (méthode en 10 planches)

But : valider **avant le code** des écrans cliquables (6 planches), que l'utilisateur
parcourt sur un canevas privé. Une référence (« comme l’appli X ») ne remplace pas la maquette.
Exemple : un dossier `maquette/` d’une appli Qt (`common.py`, planches `v*.py`),
suivi dans `docs\SUIVI.md` (« Maquette v9 : faite et publiée »). Textes : `design:ux-copy` ; relecture :
`design:design-critique`, `design:accessibility-review` ; conception d'écrans Qt : `qt-ui-design`.
Les captures et le test d'une maquette vont dans un **agent** (plus de 2-3 captures).

## 1. Organisation des sources
- **Un générateur Python par planche** : `v9_X.py` écrit `project/v9_X.dc.html` (`python v9_X.py`, dans `maquette/`).
- **Un socle commun** (`v9_common.py` + `common.py`) : jetons de couleur (`PETROL`, `SKY`, `ERR`, `OK`, `MAIN_BG`…),
  cadre d'écran (`page_v9` : écran complet 1280 px ; `board_v9` : planche libre), bandeaux, en-tête, onglets,
  helpers `btn(label, icon, primary, href, onclick)` et `ic(name)` (pictogrammes SVG). Les écrans se ressemblent
  parce qu'ils partagent ce socle : ne jamais recopier un style d'une planche à l'autre.
- **Gabarit** `T(_tpl, **kw)` : remplace chaque `[[k]]` du texte HTML/JS par `kw[k]`. Les `{{...}}` sont réservés au
  moteur et les `{}` du JS ne se mélangent pas aux `[[ ]]`, donc pas d'échappement à gérer.
  ```python
  def T(_tpl, **kw):
      s = _tpl
      for k, v in kw.items():
          s = s.replace('[[' + k + ']]', str(v))
      return s
  ```
  **Contrôle après chaque génération** : `grep -c "\[\[" project/v9_X.dc.html` doit donner `0` (un `[[k]]` resté =
  une clé oubliée).
- **`project/canvas.json`** = index du canevas (planches `x, y, w, h, title`, `is_interactive: True`,
  `expand: 'fill'` ; notes ; `order`), écrit par `write_index_v9(horodatage)` :
  `python -c "import v9_common as c; c.write_index_v9('2026-10-06T15:00:00Z')"`. Rangées de 3 planches
  (x = i × 1360, y = hauteur max de la rangée + 120). Une **note orange** porte les questions numérotées Q1, Q2…
  Garder l'ancienne version dessous (v8) pour comparer. `maquette/project/` est ignoré par git (les sources
  `.py` sont versionnées, pas les `.dc.html`).

## 2. Moteur des planches (format `.dc.html`)
- Une planche = `<x-dc>` (HTML + styles) puis `<script type="text/x-dc" data-dc-script data-props='{"$preview":
  {"width":1280,"height":N}}'>` avec `class Component extends DCLogic` : le moteur est React, mais la planche ne l'importe pas (`DCLogic`
  l'enveloppe) ; JS classique, **sans import ni TypeScript**.
  Chaque planche a son propre `state` (`this.state`, `this.setState`) ; rien n'est partagé entre planches.
- Les trous sont des **chemins pointés** `{{a.b}}`, jamais des expressions : tout calcul (libellés, classes,
  `a ? b : c`, largeurs) se fait dans `renderVals()` qui renvoie l'objet lu par le HTML. Événements :
  `onClick="{{fn}}"` avec `fn` renvoyée par `renderVals()`.
- Boucles et conditions **sans élément enveloppe** : `<sc-for list="{{rows}}" as="r" hint-placeholder-count="0">`
  et `<sc-if value="{{open}}" hint-placeholder-val="{{false}}">`.
- Aller d'une planche à l'autre : `<a href="v9_Autre.dc.html">` stylé en bouton (`btn(..., href=...)`).
- **Piège** : pas de `\u00a0` dans le JS généré (Python le transforme) → `String.fromCharCode(160)`.
- Pas de bouton ni de logique « qui n'existera pas dans l'appli » : la maquette montre le comportement réel
  (annuler/rétablir, enregistrement automatique, états vides, erreurs, fenêtres de dialogue).
- Détail du format : lire `artifact-type/reference/format.md` dans l'artefact
  (`Artifact action: read, url, path: "artifact-type/reference/format.md"`).

## 3. Vérifier AVANT de publier (jamais à l'œil seulement)
Le fichier `.dc.html` a besoin du moteur `./support.js` : c'est `artifact-type/dc-runtime.js` de l'artefact (copie
identique, vérifiée par md5) ; le lire avec `Artifact action: read, path: "artifact-type/dc-runtime.js"` puis le
poser sous le nom `support.js` à côté des planches. Servir en **http**, pas en `file://` :
```
cd maquette/project && python -m http.server 8765 --bind 127.0.0.1
```
Tests **Playwright invisibles** : `p.chromium.launch(channel='msedge', headless=True)` ; sous Windows lancer avec
`PYTHONIOENCODING=utf-8` (sinon les accents plantent l'affichage). Le logo `/_blob/...` n'existe que sur le
canevas publié : une image absente en local est attendue. Contrôles à écrire pour chaque planche :
1. **Erreurs de console** (`page.on('console')`, `pageerror`) = 0.
2. **Contenu coupé** : parcourir les conteneurs, signaler `scrollHeight > clientHeight` (ou `scrollWidth`) quand
   le CSS coupe (`overflow: hidden`) ; la hauteur annoncée dans `$preview` doit contenir toute la planche.
   **Mesurer la hauteur réelle** sur les éléments feuilles (bas du plus bas élément sans enfant), fenêtre à la
   **largeur du cadre** (1280) : `scrollHeight` du document renvoie la hauteur minimale du cadre, pas le contenu.
3. **Largeur des boutons quand un libellé change** (état, « Annuler : … », texte long) : la mise en page ne
   doit pas bouger ni couper le texte. Pastille ou bouton dont le texte peut passer sur 2 lignes :
   `min-height` + `padding` vertical, jamais `height` fixe (sinon le texte est coupé).
4. **Parcours cliqué de bout en bout** (créer, modifier, annuler, rétablir, fenêtres, liens entre planches),
   avec relevé des erreurs à chaque pas.
5. **Fond sombre** (Windows en mode sombre) : `rgba(0, 0, 0, 0)` est **transparent**, pas sombre ; calculer le
   fond effectif en remontant les parents, et vérifier que chaque texte reste lisible.
Ne jamais se connecter à claude.ai dans le navigateur pour « voir » la maquette : tout se teste en local.

## 4. Publier (outil Artifact)
- Première fois : `quickstart` (intent `design`) puis création depuis le type ; l'artefact reste **privé**.
  Le lien va dans le CLAUDE.md du projet.
- Mise à jour d'une planche : `url` de l'artefact, `root` = dossier `maquette`, `file_path` = chemin **absolu**
  de la planche (`...\maquette\project\v9_X.dc.html`). **Ne pas** remettre cette même planche dans `files` :
  erreur « appears more than once ». Forme de l'appel qui a marché :
  ```
  Artifact(action: publish, url: https://claude.ai/artifact/<id>,
           root: C:\...\mon_projet\maquette,
           file_path: C:\...\mon_projet\maquette\project\v9_X.dc.html)   # pas de "files"
  ```
- N'envoyer `project/canvas.json` **que si la disposition ou les notes changent** (règle du SUIVI ; inutile
  pour une simple correction de planche).
  Forme qui a marché (v10) : `file_path` = `...\maquette\project\canvas.json`, `files` = les planches
  (`project/v9_X.dc.html`). **Relire `canvas.json` avant** et garder toutes ses clés (dont `attachments`).
- **Clés de `files` toujours avec le préfixe `project/`** : `{"project/v9_X.dc.html": "project/v9_X.dc.html"}`.
  Une clé `v9_X.dc.html` (à la racine) crée un doublon à côté et **ne met pas à jour** la planche du canevas
  (vécu v10, version 18 perdue). Retirer un doublon : `{"v9_X.dc.html": null}` dans l'envoi suivant.
- **Vérifier ce qui est en ligne** après chaque envoi : `action: read`, `paths` = les planches envoyées, puis
  comparer leur sha256 aux fichiers locaux ; `scope: files` pour repérer un doublon.
- **Lire l'artefact** (`action: read`) avant le premier envoi d'une nouvelle conversation, sinon l'envoi est refusé.
- Après publication : noter la version dans le suivi.

## 5. Avant de présenter à l'utilisateur
- **Questions numérotées** Q1, Q2… dans la note orange du canevas ; une question = un choix net avec ses
  options et ma recommandation. Ce qui est décidé n'y figure plus.
- **Écarts entre la maquette et le plan** (ce qui a changé en dessinant : écran ajouté, champ retiré) écrits
  dans `SUIVI.md` / la SPEC, sinon le code suivra l'ancien plan.
- **Thème sombre** vérifié (contrôle 5) pour tout ce qui doit s'y afficher ; l'appli finale reste claire.
- Dire en deux lignes : lien du canevas, version, planches modifiées, questions en attente.
- **Tour de retours** (méthode validée par Nolann, « tu peux clairement garder tout ça ») :
  1) noter ses réponses dans `SUIVI.md` / la SPEC / le CLAUDE.md du projet (décisions, plan des blocs) ;
  2) modifier les sources, reconstruire, refaire les contrôles 1 à 5 et le parcours cliqué ; 3) publier une
  **nouvelle version** du même canevas ; 4) la note orange ne garde que les questions encore ouvertes (une
  dernière note « maquette vX validée » quand tout est répondu) ; 5) deux lignes : lien, version, ce qui a changé.
  Un exemple dessiné (valeur, message d'erreur) n'est qu'un exemple : ne pas le figer dans la SPEC sans le dire.
- Modifier les sources par Edit, ou par un petit script Python écrit avec Write : un heredoc bash transforme
  `\\n` en vrai retour à la ligne dans le source (chaîne non terminée), et le Python Windows ne lit pas `/c/...`.
- **Ménage après validation (Nolann, 11/10 : un Sonnet est reparti d'une maquette « entre-deux »)** : dès qu'une
  maquette est validée et finie, le faire tout de suite pour que les conversations et agents suivants ne se trompent
  pas : 1) déplacer les anciennes versions (planches, HTML, générateurs obsolètes) dans `maquette\_archive\<date>\`
  (jamais supprimer) ; 2) ne laisser que la référence et ce qui est en cours ; 3) retirer les liens morts entre
  maquettes ; 4) écrire en tête de `SUIVI.md` un bloc « MAQUETTE QUI FAIT FOI » (fichier ou lien du canevas + version,
  ce qui est archivé, ce qui reste à faire) ; 5) en cas de doute sur la référence, montrer une capture à Nolann et
  lui demander avant de dessiner.
- Pas de code d'interface tant que l'utilisateur n'a pas validé la maquette et répondu aux questions.
  Un **point maquette** (Opus ultracode, vraie appli lancée, captures, comparaison à la maquette, maquette
  mise à jour) se propose à la fin d'un jalon qui touche 3 écrans ou plus.
