## Produit physique (CAO / SolidWorks) : concevoir avant de modéliser

Workflow validé (produit physique d’origine) — **je le propose moi-même à chaque étape, sans attendre** :
1. **Schéma 2D coté du profil, à l'échelle** (SVG), refait à chaque retour jusqu'à validation ; fiche de contraintes
   dans `DESIGN.md` (cotes, fabrication, usage réel : fixation, qui voit quoi, pas de pieds si le produit est fixé).
2. **Prompts d'images pour ChatGPT / Nano Banana** dans `DESIGN.md` (ambiance, **planche de plans orthographiques**,
   coupe, détails ; base commune + schéma joint). Il génère, je lis les images comme des plans.
3. **Relire les images pour les erreurs techniques** (pièce non alimentée, chute trop haute, pente invisible, pieds
   inventés…) et écrire un prompt correctif ; ne modéliser qu'avec des plans cohérents.
4. Modélisation par étapes, une capture après chaque ; skill `solidworks-plan-vers-3d`.
Garder `DESIGN.md` et `SUIVI.md` à jour à chaque retour, et mettre à jour ce fichier / le skill quand le workflow évolue.
