---
name: creer-repo-public
description: À utiliser pour transformer un projet en BEAU dépôt public GitHub (README soigné avec captures sur données fictives, docs/, CLAUDE.md + AGENTS.md pour qu'un Claude sache l'installer et le personnaliser), avec anonymisation et scan anti-fuite avant tout push. Réutilisable pour n'importe quel projet.
---

# Créer un beau dépôt public

Exemple de référence : un dépôt public déjà publié (ton et structure à imiter).

## 1. État des lieux (avant d'écrire)
- Licence du projet et de tout code repris (upstream, bibliothèques) : l'écrire dans le README, citer l'auteur d'origine, dire à Nolann si l'usage commercial est permis. Licence absente ou douteuse = ne pas copier, prévenir.
- Chercher ce qui existe (dépôts similaires) pour s'en inspirer ; ne reprendre du texte que sous licence permissive.

## 2. Anonymiser (dans une COPIE de publication, jamais dans la source)
- Noms réels, prénoms (de personnes ET de personnages), chemins absolus personnels, e-mails, noms de projets privés, hashs de branches privées → remplacés par des génériques.
- Ajouter chaque nouveau nom privé à `mots-interdits.txt` (hors dépôt, à côté de `scan.sh`, avec limites de mot) (hors dépôt, avec limites de mot `\b`).
- Corriger aussi la source locale, sinon la prochaine synchronisation remet le nom.

## 3. Contenu du dépôt
- **README.md** (base : structure Best-README-Template, Unlicense ; contrôle final avec readme-checklist, CC0) :
  1. titre + accroche d'une phrase + badges utiles ;
  2. **Aperçu** : 2-4 captures sur DONNÉES FICTIVES (fausses conversations, faux prénoms), jamais de vraies données ;
  3. démarrage rapide (3-5 commandes copiables, testées) ;
  4. comment ça marche (schéma court) ;
  5. tableau « Je veux changer… → où » (fichier/ligne/réglage) ;
  6. FAQ / dépannage (les vrais pièges rencontrés) ;
  7. confidentialité (ce qui reste en local, ce qui sort) ;
  8. licence + crédits.
- **docs/** : `PERSONNALISER.md`, `ARCHITECTURE.md`, `DEPANNAGE.md`.
- **CLAUDE.md** (+ **AGENTS.md** court qui le référence, ou l'inverse comme dans le dépôt Optimisation : `CLAUDE.md` = `@AGENTS.md`) à la racine, pour qu'un Claude sache installer, lancer, personnaliser : commandes exactes, carte des fichiers, pièges connus. Court (< 15 Ko).
- `LICENSE`, `.gitignore` (pas de `.env`, venv, caches, captures brutes).

## 4. Captures sans navigateur installé
Méthode « canvas » (utilisée sur Bureau entreprise) : dans la page, appeler `canvas.toDataURL('image/png')` dans `requestAnimationFrame(()=>requestAnimationFrame(...))` (sinon l'image est noire) → `fetch` en POST vers un petit récepteur local (script Python `http.server` qui écrit le PNG dans `assets/`). Le récepteur (~30 lignes, `http.server`) : `do_POST` lit le corps base64 et écrit le PNG, répond avec les en-têtes CORS (`Access-Control-Allow-Origin/Methods/Headers`) et gère `OPTIONS`. Lancer le backend du dépôt avec `PYTHONPATH` sur son dossier, sinon le venv sert une autre copie du code (captures aux anciens noms). Lancer le récepteur, ouvrir l'appli sur données fictives, déclencher l'export, vérifier chaque image à l'œil (texte lisible, pas de donnée réelle). Plus de 2-3 captures → dans un agent.

## 5. Avant le push
1. `bash ~/.claude/skills/publier-repo/scan.sh <dossier>` → doit afficher PROPRE (skill `publier-repo`).
2. Relire le README rendu sur GitHub après push (images, liens, schéma).
3. **Push normal seulement.** Jamais de `--force` sans le « ok » explicite de Nolann (réécriture d'historique : voir `publier-repo`).
