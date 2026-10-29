---
name: captures-qt
description: Capturer les écrans d'une appli ou maquette PySide6 sans les afficher (offscreen), vérifier qu'ils restent identiques avec Windows en mode sombre, et mesurer les widgets par introspection plutôt qu'à l'œil. À utiliser avant de dire « fini » sur un écran Qt, pour une maquette Qt, ou pour un point maquette.
---

# Captures d'écrans Qt (PySide6) : hors écran, mode sombre, mesures

Méthode tirée d’une maquette Qt (10/10/2026). Modèle à écrire : `capture.py` et `diff_sombre.py`. Ils donnent 25 états à
1920 × 1200, et le contrôle sombre doit afficher 7 sur 7 IDENTIQUE.
Pour concevoir les écrans, voir `qt-ui-design`. Pour une maquette à faire valider sur claude.ai, voir `maquette-canevas`.

## 1. Rendre l'appli « pilotable » par état

- La fenêtre principale expose `afficher(etat)`. Cette méthode place l'appli dans un état nommé (écran, fausses données,
  dialogue ouvert) et renvoie le dialogue modal s'il y en a un, sinon `None`.
- La liste `ETATS` est dans `capture.py`. Un état qui finit par `_bas` capture l'écran défilé tout en bas.

## 2. Capturer hors écran

1. Variables d'environnement, à poser avant d'importer Qt :
   - `QT_QPA_PLATFORM=offscreen` ;
   - `QT_QPA_FONTDIR=C:\Windows\Fonts`, sans quoi les textes sortent en carrés ;
   - `QT_SCALE_FACTOR=1.5`, pour reproduire l'écran à 150 % : une fenêtre de 1280 × 800 donne une image de 1920 × 1200 ;
   - `PYTHONIOENCODING=utf-8` dans le shell.
2. Pour chaque état :
   1. créer une nouvelle fenêtre, la redimensionner, puis `show()` ;
   2. appeler `processEvents()`, puis `afficher(etat)`, puis `processEvents()` trois fois ;
   3. faire `grab()` puis `save()` ;
   4. fermer la fenêtre avec `close()` et `deleteLater()`.

   Une fenêtre neuve par état évite qu'un état déborde sur le suivant.
3. Un dialogue modal se capture à part avec `dlg.grab()`. On le colle ensuite au centre de la fenêtre, sur un voile noir
   à 60/255, avec un cadre `#767676`.
4. Pour capturer seulement quelques états : `python capture.py --etats a,b --sortie captures/_tmp`.

## 3. Contrôle « Windows en mode sombre »

- Le thème sombre de Windows casse les écrans qui se fient aux couleurs du système.
- Le contrôle consiste à capturer deux fois les mêmes états :
  - une fois normalement ;
  - une fois avec `--sombre`, qui pose une palette proche de celle de Windows sombre (`#202020` / `#2B2B2B` / texte
    `#FFFFFF`, voir `palette_sombre()` dans `capture.py`) et appelle `app.styleHints().setColorScheme(Qt.ColorScheme.Dark)`
    (Qt 6.8 ou plus).
- On compare ensuite les deux séries au pixel près avec `PIL.ImageChops.difference(...).getbbox()`.
- **Attendu : IDENTIQUE pour chaque état.** C'est le cas quand l'appli fixe elle-même son fond et son texte : style
  Fusion, palette claire explicite, et QSS avec `background` et `color`.
- Si un état est DIFFÉRENT, `diff_sombre_<etat>.png` montre la zone fautive. `diff_sombre.py` sort alors avec le code 1
  (0 si tout est IDENTIQUE) : un script peut tester ce code au lieu de lire le texte.
- Choisir au moins un état par écran, plus chaque dialogue et chaque popup.

## 4. Mesurer plutôt que regarder

Une hauteur de barre, une taille d'icône ou un alignement se vérifient par introspection, pas sur une capture :

```python
fen = FenetreX(); fen.resize(1280, 800); fen.show(); app.processEvents()
fen.afficher(etat)
for _ in range(3): app.processEvents()
print([(w.accessibleName() or "?", w.width(), w.height()) for w in fen.findChildren(QProgressBar)])
```

- **Ne pas filtrer avec `isVisible()`** : un widget d'une page de pile non affichée passerait inaperçu. C'est ainsi
  qu'une barre de 64 × 10 a été manquée une fois.
- Les tailles sont en pixels logiques, avant le facteur 1.5.
- Piège QSS : `min-height` et `max-height` portent sur le contenu, et la bordure s'y ajoute (une barre de 12 px avec
  une bordure de 1 px mesure 14 px). Fixer la hauteur dans le code avec `setFixedHeight` ou `setFixedSize`.

## 5. Regarder les captures

- Plus de 2 ou 3 images à regarder : confier la lecture à un agent Sonnet. Il lit les PNG, découpe et agrandit les zones
  douteuses avec `Image.crop`, puis rend une liste courte de défauts : texte coupé, alignement, état vide, contraste.
  Ainsi les images ne restent pas dans le fil principal.
- L'agent qui construit les écrans ne fait pas lui-même la boucle « je capture, je regarde ». La vérification visuelle
  se fait à part.

## Pièges

- Écrire les scripts avec l'outil Write, jamais avec un heredoc bash : il a déjà transformé des `\` en caractères de
  contrôle.
- Un état qui plante fait sortir `capture.py` avec un code non nul. Lire sa sortie avant de regarder les images.
