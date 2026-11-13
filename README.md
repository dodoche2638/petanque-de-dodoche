# LA PETANQUE DE DODOCHE

Application de pétanque pour Android et Windows. Elle gère les inscriptions, les poules, les tableaux A-B-C, les terrains et les résultats. Elle propose aussi le tir de précision, les entraînements, les règlements et les archives des concours.

## Version 29

Tournoi et Concours proposent le score détaillé ou le choix du gagnant, puis un cadrage si nécessaire après les poules. Le Marathon permet les inscriptions en tête-à-tête, doublette et triplette.

## Installer

Dans **Releases**, télécharger l’APK pour Android ou le ZIP Windows. Sous Windows, extraire le ZIP et ouvrir l’exécutable ou Dodoche.html. Les deux ZIP comprennent Historique-des-versions.txt.

## Organisation

- android/ contient la page de l’application Android, l’icône, le lecteur et les notices.
- windows/ contient la page Windows autonome, le lanceur C et sa table d’imports.
- scripts/ construit les deux distributions et publie les versions.
- VERSION et Historique-des-versions.txt indiquent le numéro courant et les changements par plateforme.

La base importée correspond à la v25. Les versions précédentes sont documentées dans l’historique. Les deux pages HTML sont autonomes. Pour une modification commune, reporter le changement dans les deux pages et tester les deux parcours.

## Initialiser le dépôt personnel

Créer un dépôt GitHub vide, extraire les sources, puis depuis leur dossier :

    git init -b main
    git add .
    git commit -m "Importer la version 25"
    git remote add origin URL_DU_DEPOT
    git push -u origin main

## Construire et publier une version

Sur Linux x86-64 avec Python 3, cryptography, GCC, GNU binutils, Git et GitHub CLI, configurer DODOCHE_SIGNING_KEY avec le chemin local de la clé Android d’origine. Conserver la clé hors du dépôt. Le constructeur vérifie la signature par rapport à la v25. Sans cette clé, la compilation d’une mise à jour Android compatible nécessite le poste de signature d’origine.

1. Modifier les sources et vérifier les parcours concernés sous Windows et Android.
2. Mettre à jour VERSION (numéro entier) et ajouter une entrée « v26 · Android et Windows — … » dans l’historique en adaptant le numéro et les systèmes.
3. Lancer python3 scripts/build.py. Les distributions se trouvent dans dist/.
4. Valider les changements dans un commit sur main.
5. Avec gh connecté au dépôt personnel, lancer bash scripts/publier.sh. Le script construit les fichiers, pousse le commit et le tag, joint les cinq téléchargements à un brouillon puis publie la release. Si le transfert est interrompu, relancer depuis le même commit.

Les résultats et les fichiers de licences des joueurs restent hors du dépôt. Les notices des composants tiers accompagnent les sources.
