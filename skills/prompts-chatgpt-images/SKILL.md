---
name: prompts-chatgpt-images
description: Écrire des prompts d'images pour ChatGPT / Nano Banana (coupes, planches de plans, vues d'un produit à modéliser), relire les images rendues comme des plans, rédiger les prompts correctifs. À utiliser pour tout produit physique à designer avant la CAO.
---

# Prompts d'images (ChatGPT / Nano Banana) pour un produit à modéliser

But : obtenir des images **lisibles comme des plans** (coupe, vues orthographiques), cohérentes, pour modéliser ensuite.
Projet d’origine : un produit physique conçu en CAO (prompts 1 à 8 et retours).

## Premier envoi (demande « écris-moi les prompts »)
- La réponse contient **UN seul prompt, la coupe de profil**, en anglais. Ne nomme ni ne résume aucune autre vue : écris
  seulement « les suivantes viendront après validation » ; pas de variantes, pas de planche, même si on te demande
  toutes les vues d'un coup (refuser poliment, en une phrase).
- **Cotes fournies** : les reprendre toutes, avec leur unité et leur élément, sans les remplacer ni les contredire.
  **Cotes absentes** : poser des hypothèses chiffrées marquées « Assumed, to confirm » dans le prompt et « à corriger »
  dans la réponse, et demander la fiche de contraintes.
- **Cohérence avant envoi** : vérifier que cotes, épaisseurs de paroi et porte-à-faux sont compatibles entre eux (une
  seule épaisseur de paroi, bras qui ne dépasse pas l'appui, etc.) ; ne pas ajouter d'autres cotes que celles utiles.
- **Interdits tirés de l'usage réel**, jamais copiés d'un autre produit : fixé au mur → « wall-mounted; no feet, no floor
  stand » ; posé sur un bureau → garder l'appui porteur (socle, patins), interdire seulement les fixations incompatibles
  (« no wall mount, no clamp ») ; extérieur sur piquet → « no feet, no visible screws, sealed ».

## Boucle (une image à la fois)
1. **Fiche de contraintes** dans `DESIGN.md` : cotes, matière/fabrication, usage réel (fixation, qui voit quoi, pas de pieds
   si le produit est fixé), pièces du commerce avec leurs vraies tailles.
2. **Commencer par UNE image maîtresse : la coupe de profil.** Rien d'autre tant qu'elle n'est pas bonne ; ensuite
   seulement la planche de plans (profil, face, dos, dessus, dessous), la coupe de face, les détails, l'ambiance.
3. **Lire l'image avant de répondre** : liste de contrôle ci-dessous, puis dire à Nolann ce qui est bon, ce qui est faux.
4. **Prompt correctif** = « Edit the attached image. Keep … Apply ONLY these changes: 1) … 2) … », une consigne
   numérotée par défaut constaté, **le résultat attendu et non le défaut** (« the outlet sits above the high edge of the
   tray » plutôt que « no long fall »), cotes en mm, « Deliver ONE image, same framing ».
   Mettre dans « Keep » uniquement ce qui est validé ; chaque changement numéroté traite UN défaut signalé, sans
   nouvelle exigence ni rappel de ce qui est déjà bon hors de « Keep ».
5. Écrire le prompt dans `DESIGN.md` (section « Retour »), le donner dans un bloc de code, dire quelle image joindre.
6. Ne modéliser qu'avec une image validée **par Nolann et moi**.

## Règles tirées de l'expérience
- ChatGPT **ignore une partie des consignes** (vis non retournée, angle non respecté, batterie remise au même endroit) :
  après chaque retour, **vérifier point par point** la liste envoyée et le dire. Ce qui est bon et que Nolann aime, ne pas
  le redemander ; si l'image va dans un sens acceptable, adapter la conception plutôt que de s'acharner.
- Une seule vue par prompt tant que ça ne converge pas ; joindre l'image à corriger et, si besoin, mon schéma.
- Base commune en anglais (produit, cotes, matière, **interdits : pas de pieds, pas de vis visibles…**) à répéter au début
  de chaque prompt de la série.
- Style : aplats / rendu technique, fond blanc, pas de perspective pour les plans ; pièces amovibles dessinées comme pièces
  distinctes avec jeux fins ; pas d'étiquettes ni de texte.

## Liste de contrôle quand je lis une image comme un plan
- La pièce est-elle **alimentée** (comment la matière entre dans le mécanisme) ? hauteur de chute, point d'impact ?
- Pentes visibles et dans le bon sens ? angles proches des cotes demandées ?
- Entraînement **cohérent** (axes moteur/vis parallèles ou bien accouplés ; engrenages possibles) ?
- **Accès** pour changer les pièces interchangeables et les consommables (batterie, vis) : où, par quel capot ?
- Pièces du commerce à la bonne taille et au bon endroit ? Pieds, prises, vis inventés ? Zones floues non identifiables ?
- Murs, jeux, joints plausibles pour la fabrication visée (FDM : parois ≥ 1,6, surplombs ≤ 45°) ?

## Plus tard (idée de Nolann, hypothétique)
Si un accès direct à ChatGPT devient possible (navigateur piloté, « Open Claude »), enchaîner moi-même
prompt → image → lecture avec la liste ci-dessus → correctif, **5 tours au plus** avant de rendre la main avec les
images et les points restants ; garder DESIGN.md à jour à chaque tour.
