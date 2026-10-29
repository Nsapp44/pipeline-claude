---
name: verif-responsive-web
description: Vérifier le responsive d'une page web (mobile 375, tablette 768, grand écran 1440) avec le navigateur intégré avant de dire « fait ». À utiliser à chaque changement d'interface sur un site (Astro, React, HTML).
---

# Vérification responsive (site web)

Obligatoire avant « fait » sur toute page ou composant modifié.

1. Serveur local lancé (`astro dev` / Docker). Ouvrir la page dans le navigateur intégré (`navigate`).
2. Pour chaque taille : `resize_window` preset `mobile` (375×812), `tablet` (768×1024), puis `desktop`
   (et un grand écran custom 1440×900 si la mise en page a un `max-width`).
3. À chaque taille, recharger la page, puis :
   - `javascript_exec` : `({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth})`
     → `sw` doit égaler `cw` (aucun scroll horizontal).
   - `scrollIntoView` sur l'élément modifié, puis capture (`scale` 0.5-0.6).
4. Regarder : texte coupé, éléments qui se chevauchent, boutons < 44 px de haut sur mobile, images qui
   débordent, états vides / erreur, et que les îlots React sont bien hydratés (cliquer un bouton).
5. Thème sombre de Windows : le site fixe ses propres couleurs ; `resize_window` avec `colorScheme: "dark"`
   pour contrôler qu'aucun fond/texte ne reste « par défaut ».
6. Animations : doivent rester celles du site (entrée `translateY(6px)` 0,5 s) et respecter
   `prefers-reduced-motion`.
7. Toujours `resize_window` preset `desktop` à la fin.

Rapport : une ligne par taille (OK / problème), captures montrées à Nolann. Plus de 2-3 captures → agent `testeur`.
Piège : une capture prise pendant l'animation d'entrée paraît vide ; attendre 1 s ou scroller.
