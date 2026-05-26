import threading
import tkinter
import os
import customtkinter
import yt_dlp
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import filedialog

def sanitize_filename(filename):
    """Nettoie une chaîne de caractères pour le nom de fichier."""
    return "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_", "-")).rstrip()

class YTDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("720x600")
        self.master.title("YT Downloader + (yt-dlp Edition)")

        customtkinter.set_appearance_mode("System")

        self.flStop = False
        self.download_path = os.getcwd()
        self.video_info = None
        self.selected_quality = tkintermente = tkinter.StringVar(value="Sélectionner la qualité")
        self.selected_audio_format = tkinter.StringVar(value="Non")

        # --- UI Setup ---
        self.frameIdentification = customtkinter.CTkFrame(self.master, width=700, height=240)
        self.frameIdentification.pack(fill="both", side="top", pady=10, padx=10)

        self.labelMiniature = customtkinter.CTkLabel(self.frameIdentification, width=380, height=220, text=None)
        self.labelMiniature.pack(side="left", padx=10, pady=10)

        self.frameDetails = customtkinter.CTkFrame(self.frameIdentification, width=300, height=240)
        self.frameDetails.pack(fill="both", padx=10, pady=10, expand=True, anchor="n")

        self.labelTitre = customtkinter.CTkLabel(self.frameDetails, text="Titre : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
        self.labelTitre.pack(padx=10, fill="both", side="top", expand=True)

        self.labelAuteur = customtkinter.CTkLabel(self.frameDetails, text="Auteur : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
        self.labelAuteur.pack(padx=10, fill="both", side="top", expand=True)

        self.labelDuree = customtkinter.CTkLabel(self.frameDetails, text="Duree : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
        self.labelDuree.pack(padx=10, fill="both", side="top", expand=True)

        self.labelVues = customtkinter.CTkLabel(self.frameDetails, text="Vues : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
        self.labelVues.pack(padx=10, fill="both", side="top", expand=True)

        self.frameDownloader = customtkinter.CTkFrame(self.master, width=700, fg_color="transparent")
        self.frameDownloader.pack(fill="both", expand=True, pady=(0,10))

        self.urlValue = tkinter.StringVar()
        self.urlValue.trace_add("write", self.onChangeURL)
        self.labelLink = customtkinter.CTkEntry(self.frameDownloader, textvariable=self.urlValue, corner_radius=10, width=400, height=40, border_color="#4180A2")
        self.labelLink.pack(pady=2lemma=20)

        self.frameOptions = customtkinter.CTkFrame(self.frameDownloader, fg_color="transparent")
        self.frameOptions.pack(pady=5)

        self.quality_optionmenu = customtkinter.CTkOptionMenu(self.frameOptions, variable=self.selected_quality, values=["Sélectionner la qualité"])
        self.quality_optionmenu.pack(side="left", padx=10)

        self.audio_optionmenu = customtkinter.CTkOptionMenu(self.frameOptions, variable=self.selected_audio_format, values=["Non", "Télécharger l'audio"])
        self.audio_optionmenu.pack(side="left", padx=10)

        self.download_path_button = customtkinter.CTkButton(self.frameOptions, text="Choisir le dossier", command=self.select_download_append_path)
        self.download_path_button.pack(side="left", padx=10)

        self.current_download_path_label = customtkinter.CTkLabel(self.frameDownloader, text=f"Dossier: {self.download_path}")
        self.current_download_path_label.pack(pady=5)

        self.labelPercent = customtkinter.CTkLabel(self.frameDownloader, text="0%")
        self.labelPercent.pack()

        self.progressBar = customtkinter.CTkProgressBar(self.frameDownloader, width=500, progress_color="#41A253")
        self.progressBar.set(0)
        self.progressBar.pack()

        self.frameButtons = customtkinter.CTkFrame(self.frameDownloader, width=520, height=100, fg_color="transparent")
        self.frameButtons.pack(pady=15)

        self.buttonDownload = customtkinter.CTkButton(self.frameButtons, text="Download", corner_radius=30, command=self.onClickDownload, hover_color="#41A253", fg_color="#4180A2")
        self.buttonDownload.pack(side="left", padx=15)

        self.buttonCancel = customtkinter.CTkButton(self.frameButtons, text="Cancel", corner_radius=30, command=self.onClickCancel, hover_color="#CA4A4A", fg_color="#4180A2")
        self.buttonCancel.pack(side="right", padx=15)

        self.finishLabel = customtkinter.CTkLabel(self.frameDownloader, text="", font=("Helvetica", 12, "bold"))
        self.finishLabel.pack()

    def getThumbnail(self, thumbnailLink):
        try:
            response = requests.get(thumbnailLink, timeout=5)
            img = Image.open(Byteslob := BytesIO(response.content))
            img = img.resize(size=(380, 220))
            return ImageTk.PhotoImage(img)
        except:
            return None

    def updateIDVideo(self, info):
        self.labelTitre.configure(text="Titre : " + info.get('title', 'N/A'))
        self.labelAuteur.configure(text="Auteur : " + info.get('uploader', 'N/A'))
        duration = info.get('duration', 0)
        self.labelDuree.configure(text=f"Duree : {int(duration // 60)} min")
        views = info.get('view_count', 0)
        self.labelVues.configure(text=f"Vues : {round(views / 1000, 2)} k")
        
        img = self.getThumbnail(thumbnailLink=info.get('thumbnail'))
        if img: self.labelMiniature.configure(image=img)

        # Extract resolutions
        formats = info.get('formats', [])
        qualities = []
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('height'):
                res = f"{f['height']}p"
                if res not in qualities: qualities.append(res)
        
        self.video_qualities = sorted(qualities, key=lambda x: int(x[:-1]), reverse=True)
        
        if self.video_qualities:
            self.quality_optionmenu.configure(values=self.video_qualities)
            self.selected_quality.set(self.video_qualities[0])
        else:
            self.quality_optionmenu.configure(values=["Aucune qualité"])

        # Audio options
        audio_opts = ["Non"]
        for f in formats:
            if f.get('acodec') != 'none' and f.get('abr'):
                audio_opts.append(f"Audio ({f['abr']} kbps)")
        self.audio_optionmenu.configure(values=list(set(audio_opts)))

    def resetIDVideo(self):
        self.labelTitre.configure(text="Titre : ")
        self.labelAuteur.configure(text="Auteur : ")
        self.labelDuree.configure(text="Duree : ")
        self.labelVues.configure(text="Vues : ")
        self.labelMiniature.configure(image=None)
        self.quality_optionmenu.configure(values=["Sélectionner"])
        self.audio_optionmenu.configure(values=["Non"])

    def select_download_append_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.current_download_append_path_label.configure(text=f"Dossier: {self.download_path}")

    def onChangeURL(self, *args):
        url = self.urlValue.get()
        if not url:
            self.resetIDVideo()
            return

        def fetch():
            try:
                ydl_opts = {'quiet': True, 'noplaylist': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    self.video_info = info
                    self.master.after(0, lambda: self.updateIDVideo(info))
                    self.master.after(0, lambda: self.finishLabel.configure(text="", text_color="white"))
            except Exception as e:
                self.master.after(0, self.resetIDVideo)
                self.master.after(0, lambda: self.finishLabel.configure(text="Lien invalide ou erreur", text_color="#CA4A4A"))

        threading.Thread(target=fetch, daemon=True).start()

    def onClickDownload(self):
        if not self.video_info:
            self.finishLabel.configure(text="Chargez d'abord une vidéo !", text_color="#CA4A4*A")
            return
        
        self.flStop = False
        self.progressBar.set(0)
        self.labelPercent.configure(text="0%")
        self.finishLabel.configure(text="Téléchargement en cours...", text_color="white")
        
        url = self.urlValue.get()
        threading.Thread(target=self.download_process, args=(url,), daemon=True).start()

    def download_process(self, url):
        try:
            quality = self.selected_quality.get()
            is_audio = self.selected_audio_format.get() != "Non"
            sanitized_title = sanitize_filename(self.video_info.get('title', 'video'))
            
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, f'{sanitized_title}.%(ext)s'),
                'progress_hooks': [self.progress_hook],
            }

            if is_audio:
                ydl_opts['format'] = 'bestaudio/best'
            else:
                ydl_opts['format'] = f'bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if not self.flStop:
                self.master.after(0, lambda: self.finishLabel.configure(text="Terminé !", text_color="#41A253"))

        except Exception as e:
            msg = str(e)
            if "Annulation" in msg:
                self.master.after(0, lambda: self.finishLabel.configure(text="Annulé !", text_color="#EA9544"))
            else:
                self.master.after(0, lambda: self.finishLabel.configure(text=f"Erreur: {msg[:30]}", text_color="#CA4A4A"))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%', '')
            try:
                perc = float(p_str) / 100
                self.master.after(0, lambda: self.progressBar.set(perc))
                self.master.after(0, lambda: self.labelPercent.configure(text=f"{p_str}%"))
            except: pass
        if self.flStop:
            raise Exception("Annulation")

    def onClickCancel(self):
        self.flStop = True

if __name__ == "__main__":
    app = customtkinter.CTk()
    yt_app = YTDownloaderApp(app)
    app.mainloop()