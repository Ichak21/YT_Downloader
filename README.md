# 🚀 YT Downloader Plus

![GUI of YT Downloader Plus](img/image.png)

**YT Downloader Plus** est une application de bureau moderne et intuitive conçée pour télécharger facilement des vidéos et de l'audio depuis YouTube. Grâce à une interface graphique fluide (CustomTkinter), l'utilisateur bénéficie d'un contrôle total sur la qualité de ses téléchargements.

## ✨ Fonctionnalités (Version 2.1)

### 📥 Téléchargement Flexible
* **Vidéo Haute Qualité** : Téléchargez la vidéo complète (vidéo + audio) dans la résolution souhaitée (ex: 1080p, 720p). Le fichier de sortie sera au format MP4 avec des codecs universellement compatibles.
* **Extraction Audio** : Option dédiée pour télécharger uniquement la piste audio au format MP3.
* **Multi-format** : Utilisation du moteur `yt-dlp` pour une compatibilité maximale et une stabilité optimale face aux changements de YouTube.

### 🔍 Prévisualisation & Détails
* **Analyse Instantanée** : Dès que l'URL est collée, l'application récupère automatiquement :
    * Le titre de la vidéo.
    * Le nom de l'auteur (chaîne).
    * La durée de la vidéo.
    * Le nombre de vues.
    * La miniature (thumbnail) en haute résolution.

### 🛠️ Contrôle & Expérience Utilisateur
* **Gestion du Dossier** : Choisissez précisément le répertoire de destination pour vos fichiers.
* **Progression en Temps Réel** : La barre de progression et l'indicateur de pourcentage affichent désormais l'avancement de manière fiable, y compris pendant les phases de post-traitement (fusion/conversion).
* **Annulation Intelligente** : Possibilité d'interrompre un téléchargement en cours avec suppression automatique du fichier partiel pour éviter les fichiers corrompus.
* **Robustesse** : 
    * Nettoyage automatique des caractères spéciaux dans les noms de fichiers pour éviter les erreurs système.
    * Gestion d'erreurs détaillée (Lien invalide, vidéo indisponible, etc.) avec feedback visuel (couleurs rouge/orange/vert).

---

## 🛠️ Installation & Configuration

### Prérequis
* **Python 3.x**
* Les bibliothèques suivantes (installables via pip) :
  ```bash
  pip install customtkinter yt-dlp requests Pillow
  ```
* **FFmpeg** : Nécessaire pour la fusion des flux vidéo/audio et la conversion des formats. Téléchargez-le depuis le [site officiel de FFmpeg](https://ffmpeg.org/download.html). Assurez-vous que `ffmpeg.exe` et `ffprobe.exe` sont disponibles dans votre PATH système ou spécifiez le chemin complet dans le code de l'application (actuellement configuré sur `C:\ffmpeg\bin\ffmpeg.exe` pour Windows).

### Utilisation
1. Lancez l'application :
   ```bash
   python YTdownloader.py
   ```
2. Collez l'URL YouTube dans le champ de saisie.
3. Attendez l'affichage des détails de la vidéo.
4. Sélectionnez la **qualité vidéo** désirée pour télécharger la vidéo complète (avec image et son). Si vous souhaitez uniquement télécharger l'audio, sélectionnez l'option **"Télécharger Audio Seulement"** dans le menu déroulant dédié.
5. (Optionnel) Cliquez sur **"Choisir le dossier"** pour changer la destination.
6. Cliquez sur **"Download"** et suivez la progression !

---

## ⚙️ Technologies Utilisées
* **Interface Graphique** : `CustomTkinter` (UI moderne et adaptative).
* **Moteur de téléchargement** : `yt-dlp` (moteur robuste pour l'extraction de flux).
* **Traitement d'images** : `Pillow` & `requests` (gestion des miniatures).
* **Concurrence** : `threading` (pour garantir une interface fluide et non bloquante).

---

*Note : La capture d'écran (img/image.png) devra être mise à jour pour refléter l'interface actuelle et les dernières fonctionnalités.*