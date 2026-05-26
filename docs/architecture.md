# Architecture Technique : YT Downloader Plus

## 1. Introduction

L'application `YT Downloader Plus` est une application de bureau Python orientée objet. Elle utilise `CustomTkinter` pour son interface graphique moderne et s'appuie sur un système de threading pour gérer le téléchargement, garantissant une interface utilisateur fluide et non bloquante. La version 2.1 a migré de `pytube` vers `yt-dlp` pour assurer une stabilité maximale face aux mises à jour de YouTube.

## 2. Diagramme d'Architecture (V2.1)

```mermaid
graph TD
    subgraph "User Interaction"
        A[Utilisateur]
    end

    subgraph "Application GUI (YTDownloaderApp Class - Main Thread)"
        B[Interface Graphique - customtkinter]
        B -- Colle URL --> C{onChangeURL}
        C -- Met à jour --> D[Détails Vidéo]
        C -- Récupère & Popule --> E[Sélecteur Qualité Vidéo (CTkOptionMenu)]
        C -- Récupère & Popule --> F[Sélecteur Audio Uniquement (CTkOptionMenu)]
        B -- Clique 'Choisir le dossier' --> G{select_download_path}
        G -- Met à jour --> H[Label Dossier de Téléchargement]
        B -- Clique 'Download' --> I{onClickDownload}
        B -- Clique 'Cancel' --> J{onClickCancel}
        K[Barre de Progression]
        L[Label de Statut]
    end

    subgraph "Background Process (Download Thread)"
        M[Download Thread]
        N[yt-dlp]
        O{progress_hook}
    end

    subgraph "Application State"
        P[flStop Flag]
        Q[video_info (dict)]
        R[selected_quality]
        S[selected_audio_format]
        T[download_path]
    end

    A --> B
    I -- Lance --> M
    M -- Utilise --> N
    N -- Appelle --> O
    O -- Met à jour --> K
    M -- Terminé/Erreur --> L
    J -- Modifie --> P
    M -- Vérifie --> P
    I -- Lit --> Q
    I -- Lit --> R
    I -- Lit --> S
    I -- Lit --> T
    C -- Met à jour --> Q
    C -- Met à jour --> E
    C -- Met à jour --> F
    G -- Met à jour --> T
```

## 3. Composants Principaux

### Application (YTDownloaderApp)
L'application est structurée autour d'une classe `YTDownloaderApp` qui encapsule toute la logique de l'interface utilisateur et de l'orchestration du téléchargement. Cette approche orientée objet améliore la maintenabilité et l'évolutivité du code.

### Interface Utilisateur (GUI)
Construite avec `CustomTkinter`, l'interface s'exécute sur le thread principal. Elle est responsable de la capture des entrées utilisateur et de l'affichage de l'état. Les fonctionnalités clés incluent :
- Un `CTkOptionMenu` pour la sélection de la **qualité vidéo** (résolutions disponibles). `onChangeURL` récupère et popule dynamiquement les options.
- Un `CTkOptionMenu` pour le **téléchargement audio uniquement**, permettant de choisir la qualité audio (abr).
- Un `CTkButton` "Choisir le dossier" qui utilise `tkinter.filedialog` pour permettre à l'utilisateur de définir le **répertoire de téléchargement**.

### Logique de Téléchargement
La bibliothèque `yt-dlp` gère toute l'interaction avec YouTube. Elle est utilisée pour extraire les informations (`extract_info`) et gérer le téléchargement (`download`). 
- L'application utilise un `progress_hook` pour intercepter les événements de téléchargement de `yt-dlp` (pourcentage, vitesse, etc.) et mettre à jour la barre de progression en temps réel.
- Pour éviter les erreurs système, le titre de la vidéo est nettoyé via `sanitize_filename`.

### Gestion des Threads
Pour garantir que l'interface utilisateur reste réactive pendant le téléchargement, la fonction `onClickDownload` lance le processus dans un thread séparé (`threading.Thread`). Cela empêche l'application de "geler" pendant la récupération des données ou le téléchargement du fichier.

### Mécanisme d'Annulation
Un drapeau (`self.flStop`) est utilisé pour communiquer entre le thread principal et le thread de téléchargement. Le thread de téléchargement vérifie périodiquement ce drapeau et interrompt le processus si `self.flStop` est `True`, supprimant le fichier partiellement téléchargé pour laisser le répertoire propre.

### Gestion des Erreurs et Feedback
Des améliorations ont été apportées à la gestion des erreurs, fournissant des messages plus spécifiques à l'utilisateur (Lien invalide, vidéo indisponible, erreur réseau) avec un feedback visuel par couleurs (rouge/orange/vert).

## 4. Packaging
Le fichier `app_v1.spec` est la configuration pour `PyInstaller`. Il est utilisé pour packager le script Python et ses dépendances en un exécutable autonome pour Windows.

## 5. Dépendances Externes
- `customtkinter`
- `yt-dlp`
- `requests`
- `Pillow`
- `tkinter.filedialog` (module standard Python)