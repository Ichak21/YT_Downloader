# Contexte du Projet : YT Downloader Plus

## 1. Objectif du Projet

Ce projet fournit une application de bureau simple avec une interface graphique pour télécharger des vidéos depuis YouTube. L'utilisateur peut coller une URL, voir les détails de la vidéo et lancer le téléchargement, avec des options avancées de qualité vidéo ou audio, et la possibilité d'annuler en cours de route.

## 2. État Actuel

-   **Version** : 2.1
-   **Fonctionnalités** :
    -   Téléchargement de vidéos via une URL.
    -   Prévisualisation des détails de la vidéo (titre, auteur, durée, vues, miniature).
    -   **Nouveau :** Sélection de la qualité vidéo (ex: 1080p, 720p).
    -   **Nouveau :** Option de téléchargement audio uniquement (ex: en format MP3).
    -   **Nouveau :** Choix du répertoire de téléchargement.
    -   Barre de progression du téléchargement.
    -   Possibilité d'annuler un téléchargement en cours.
    -   Gestion améliorée des erreurs pour un feedback utilisateur plus précis.
    -   **Correction :** Amélioration de la fiabilité de la barre de progression pour tous les types de téléchargements.
    -   **Correction :** Gestion améliorée des formats de sortie pour garantir des fichiers MP4 lisibles (codec H.264) pour les vidéos et MP3 pour l\"audio, en résolvant les problèmes de fichiers illisibles dus aux conversions incorrectes de flux audio en vidéo.
    -   **Amélioration UI :** Clarification des libellés des options de sélection audio/vidéo pour une meilleure compréhension utilisateur.

## 3. Technologies Principales

-   **Langage** : Python
-   **Interface Graphique (GUI)** : `Tkinter` / `CustomTkinter`
-   **Interaction YouTube** : `yt-dlp` (moteur haute performance et stable)
-   **Gestion des images** : `requests`, `Pillow (PIL)`
-   **Sélection de fichiers/dossiers** : `tkinter.filedialog`
-   **Packaging** : `PyInstaller`

## 4. Structure du Dépôt

-   `YTdownloader.py`: Script principal de l'application (orienté objet).
-   `README.md`: Informations générales sur le projet.
-   `.roorules`: Règles pour l'agent IA.
-   `app_v1.spec`: Fuit de configuration pour `PyInstaller`.
-   `img/`: Dossier contenant les images pour la documentation.
-   `.gitignore`: Fichiers et dossiers à ignorer avec Git.

## 5. Instructions pour l'Agent

**Règle Fondamentale** : Après chaque série de modifications validées (code ou documentation), les fichiers `context.md` et `docs/architecture.md` doivent être mis à jour pour refléter avec précision les changements et les décisions prises.