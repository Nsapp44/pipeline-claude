---
name: verif-pixel
description: Contrôle au pixel d'un écran livré (web ou Qt) contre la maquette validée, rapport texte, image d'écart seulement si le seuil est dépassé. À lancer avant toute capture "vue par le modèle" d'un écran.
---

# verif-pixel

Compare une capture à la maquette de référence sans regarder d'image : rapport TEXTE.

## Usage

```
python ~/.claude/skills/verif-pixel/verif_pixel.py --ref maquette.png --actual capture.png --out <dossier_sortie> [--seuil-pct 0.5] [--tolerance 8] [--grille 8]
```

- `--seuil-pct` : % de pixels différents toléré (défaut 0.5).
- `--tolerance` : écart par canal RVB toléré, anti-aliasing (défaut 8).
- `--grille` : découpe NxN pour localiser les écarts (défaut 8).

## Codes de sortie

- 0 : % différent <= seuil (OK).
- 1 : seuil dépassé ; `ecart.png` écrit (ref | actual | masque rouge, <= 1600 px de large).
- 2 : tailles différentes (aucun redimensionnement silencieux) ; recapturer à la taille de la maquette.

## Rapport

`rapport.txt` (<= 15 lignes, aussi sur stdout) : verdict, % global, 5 cellules les plus fautives avec % et coordonnées en pixels (x0,y0-x1,y1).

## Règles

- L'agent ne regarde une image QUE pour les zones en écart (ouvrir `ecart.png` ou rogner la cellule citée). Les captures restent nécessaires pour le jugement de design : ce skill prouve la conformité, pas la qualité.
- Qt : comparer aussi en mode sombre de Windows (maquette et capture dans le même mode).
- Le script ne modifie aucun fichier du projet : il n'écrit que dans le dossier `--out` donné (le choisir hors du dépôt, ex. scratchpad).
- Mode lot : `--ref <dossier> --actual <dossier>` compare tous les PNG de même nom (une ligne OK/ECART par fichier). Si écart : `zoom1-3.png` = bbox des 3 pires cellules, rognée +20 px, ×2 (ref | actual); `--ignore-bord N`, `--zoom X`, à ouvrir à la place des images entières.
- Capture web : `PW_ROOT=<dossier avec node_modules/playwright-core> node capture_pw.cjs <url> <out.png> [larg] [haut] [light|dark] [sélecteur]` (Chrome headless, aucun coût modèle). Enchaîner capture puis verif_pixel dans le même Bash. Qt : `captures-qt`.
