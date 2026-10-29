---
name: installateur-msi
description: Construire un installateur Windows .msi propre (WiX 5) pour une appli Python/PyInstaller, avec vrais écrans d'installation (bienvenue, dossier, raccourcis Menu Démarrer / Bureau, progression, fin avec « Lancer l'appli » coché). À utiliser dès qu'on doit livrer une appli Windows à des utilisateurs, ou refaire un installateur sur le modèle d'Approtatio.
---

# Installateur .msi (modèle : `installateur/` d’un projet existant)

Fichiers de référence à écrire sur le modèle d’un projet existant : un `.wxs` et un `construire_msi.bat` dans `installateur/`.

## Prérequis (une fois par PC)
- SDK .NET 8, puis `dotnet tool install --global wix` (WiX 5.0.2).
- Extension d'interface : `wix extension add --global WixToolset.UI.wixext/5.0.2`.
- PATH du script : `C:\Program Files\dotnet` et `%USERPROFILE%\.dotnet\tools`.

## Principes
- **Par utilisateur, sans droits admin** : `Scope="perUser"`, dossier `LocalAppDataFolder\Programs\<Appli>`, clés en HKCU.
- **PyInstaller en dossier** (pas onefile), construit dans `%TEMP%` pour ne pas salir le dossier de dev ; le `.msi`
  va dans `installateur\sortie\` (ignoré par git). `<Files Include="$(var.Source)\**" />` (WiX ≥ 5).
- **UpgradeCode fixe pour toujours** ; **augmenter `Version` à chaque livraison** (MajorUpgrade remplace en place,
  sinon l'installation « ne fait rien »). GUID de composants fixes, un par composant.
- Construction : `wix build X.wxs -ext WixToolset.UI.wixext -culture fr-FR -d Source=<dist> -arch x64 -o sortie\X.msi`
  (`-culture fr-FR` = textes standard en français).

## Interface (ce que l'utilisateur attend, comme tous les installeurs)
`<ui:WixUI Id="WixUI_InstallDir" InstallDirectory="INSTALLFOLDER" />` (xmlns:ui=`http://wixtoolset.org/schemas/v4/wxs/ui`) donne :
Bienvenue → Dossier → Prêt → **barre de progression** → Fin. On ajoute :
- **Écran Raccourcis** (`Dialog` perso, 370×270, bannière et libellés `!(loc.…)` standard) : cases Menu Démarrer et
  Bureau, propriétés `RACCOURCI_DEMARRER` / `RACCOURCI_BUREAU` = 1 (cochées par défaut) ; chaque raccourci est dans un
  composant à `Condition="RACCOURCI_… = 1"` (avec une valeur HKCU comme KeyPath).
- **Pas d'écran de licence** : publier des `NewDialog` avec un `Order` plus grand que ceux de WixUI (le plus grand gagne,
  les originaux restent dans la table) : Welcome.Next→InstallDir, InstallDir.Back→Welcome, InstallDir.Next→Raccourcis,
  VerifyReady.Back→Raccourcis.
- **Case « Lancer <Appli> » cochée à la fin** : `WIXUI_EXITDIALOGOPTIONALCHECKBOX=1`,
  `WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT`, `CustomAction` (`Return="asyncNoWait"`, ExeCommand entre guillemets) publiée
  sur `ExitDialog.Finish` avec `WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1 AND NOT Installed`.
- **Épingler** à la barre des tâches / au Démarrer : **impossible par programme** (Windows l'interdit). Le raccourci du
  Menu Démarrer rend l'appli trouvable dans la recherche ; l'écran Raccourcis explique « clic droit → Épingler ».

## Personnalisation (images et textes)
- Images BMP 24 bits : bannière **493×58** (`WixUIBannerBmp`), accueil/fin **493×312** (`WixUIDialogBmp`, bandeau gauche de
  164 px, le texte est à droite). `<WixVariable Id="..." Value="$(sys.SOURCEFILEDIR)images/x.bmp" />` — **barres obliques**
  (un antislash suivi de b ou a dans un outil d'édition devient un caractère de contrôle). Générer par script (Qt hors écran :
  `QImage.convertToFormat(Format_RGB888).save(..., "BMP")`) ; l'écran Raccourcis perso reprend la bannière tout seul.
- Textes : fichier `.wxl` (`<String Id="WelcomeDlgTitle" Value="{\WixUI_Font_Bigger}…"/>`) passé par `-loc`, mêmes
  identifiants que WixUI : WelcomeDlgTitle/Description, InstallDirDlgTitle/Description, VerifyReadyDlgInstallTitle/Text,
  ProgressDlgTitleInstalling/TextInstalling, ExitDialogTitle/Description. Garder le préfixe de police des titres.
- Vérifier avec `msilib` (Python) sur la table `Control` ; pas avec le COM PowerShell (renvoie des nombres).
- Impossible à changer : couleurs, polices, forme des boutons (fenêtres Win32 standard).

## Tests (sans captures d'écran)
- Compiler, puis installation silencieuse : `msiexec /i X.msi /qn /l*v journal.log`, vérifier l'exe, les deux
  raccourcis (.lnk) et les clés HKCU ; désinstaller `/x … /qn` et vérifier qu'il ne reste **rien**.
- Vérifier le flux des écrans dans la table `ControlEvent` (COM `WindowsInstaller.Installer`, requête SQL).
- Le rendu visuel (texte qui déborde) se vérifie par **l'utilisateur** ou par une capture d'**une seule fenêtre**.
- **Interdit** : `SendKeys` à l'aveugle et captures d'écran entières (elles montrent le bureau de l'utilisateur et les
  touches peuvent partir dans une autre fenêtre).

## Signature (avertissement « éditeur inconnu » de SmartScreen)
- Sans certificat, le .msi est non signé : avertissement sur les PC où il est téléchargé ; à la main (clé USB/réseau)
  c'est discret. Auto-signé : l'avertissement reste, sauf à installer le certificat sur chaque PC.
- Vraies options : SignPath Foundation (gratuit, dépôt public + licence libre + CI), Azure Trusted Signing, certificat
  acheté. Ne jamais publier un dépôt sans accord explicite de l'utilisateur (voir mémoire `feedback-depot-public`).
- Une signature déjà posée ne disparaît pas si on supprime le certificat ; un .msi reconstruit est non signé.

## Pièges
- Doublons de dialogues WixUI : ne pas redéfinir un dialogue existant, passer par des `Publish` d'Order supérieur.
- Caractères accentués dans les textes : le .wxs est en UTF-8 ; `Codepage="1252"` pour le français.
- Association de fichiers : clés HKCU `Software\Classes\.ext` et `Software\Classes\<ProgId>` (pas besoin d'admin).
- Une désinstallation qui laisse des clés = composant sans KeyPath HKCU ; toujours tester le nettoyage.
