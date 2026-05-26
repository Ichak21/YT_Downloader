# Contexte du Projet : YT Downloader Plus

## 1. Objectif du Projet

Ce projet fournit une application de bureau simple avec une interface graphique pour télécharger des vidéos depuis YouTube. L'utilisateur peut coller une URL, voir les détails de la vidéo et lancer le téléchargement, avec une option pour l'annuler en cours de route.

## 2. État Actuel

-   **Version** : 1.0
-   **Fonctionnalités** :
    -   Téléchargement de vidéos via une URL.
    -   Prévisualisation des détails de la vidéo (titre, auteur, durée, vues, miniature).
    -   Barre de progression du téléchargement.
    -   Possibilité d'annuler un téléchargement en cours.
-   **Bug Connu** : L'annulation du téléchargement échoue si le titre de la vidéo contient certains caractères spéciaux, empêchant la suppression du fichier temporaire.
-   **Roadmap (v2.0)** :
    -   Correction du bug des caractères spéciaux.
    -   Ajout d'options de téléchargement (audio uniquement, sélection de la qualité vidéo).

## 3. Technologies Principales

-   **Langage** : Python
-   **Interface Graphique (GUI)** : `Tkinter` / `CustomTkinter`
-   **Interaction YouTube** : `pytube`
-   **Gestion des images** : `requests`, `Pillow (PIL)`
-   **Packaging** : `PyInstaller`

## 4. Structure du Dépôt

-   `YTdownloader.py`: Script principal de l'application.
-   `README.md`: Informations générales sur le projet.
-   `.roorules`: Règles pour l'agent IA.
-   `app_v1.spec`: Fichier de configuration pour `PyInstaller`.
-   `img/`: Dossier contenant les images pour la documentation.
-   `.gitignore`: Fichiers et dossiers à ignorer par Git.

## 5. Instructions pour l'Agent

**Règle Fondamentale** : Après chaque série de modifications validées, les fichiers `context.md` et `docs/architecture.md` doivent être mis à jour pour refléter avec précision les changements et les décisions prises.
