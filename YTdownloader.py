import threading
import re
import tkinter
import os
import customtkinter
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import filedialog

def sanitize_filename(filename):
    """
    Nettoie une chaîne de caractères pour la rendre utilisable comme nom de fichier.
    Supprime les caractères interdits.
    """
    return "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_", "-")).rstrip()

class YTDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("720x600") # Increased height to accommodate new controls
        self.master.title("YT Downloader +")

        customtkinter.set_appearance_mode("System")

        self.flStop = False
        self.download_path = os.getcwd()
        self.ytObject = None
        self.available_streams = []
        self.video_qualities = []
        self.audio_streams = []
        self.selected_quality = tkinter.StringVar(value="Sélectionner la qualité")
        self.selected_audio_format = tkinter.StringVar(value="Non")

        # Frame identification video
        self.frameIdentification = customtkinter.CTkFrame(self.master, width=700, height=240)
        self.frameIdentification.pack(fill="both", side="top", pady=10, padx=10)

        self.labelMiniature = customtkinter.CTkLabel(self.frameIdentification, width=380, height=220, fg_color="transparent", text=None)
        self.labelMiniature.pack(side="left", padx=10, pady=10)

        # Sub Frame for details of video
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

        # Frame de control pour download
        self.frameDownloader = customtkinter.CTkFrame(self.master, width=700, fg_color="transparent") # Removed fixed height
        self.frameDownloader.pack(fill="both", expand=True, pady=(0,10))

        self.urlValue = tkinter.StringVar()
        self.urlValue.trace("w", self.onChangeURL)
        self.labelLink = customtkinter.CTkEntry(self.frameDownloader, textvariable=self.urlValue, corner_radius=10, width=400, height=40, border_color="#4180A2")
        self.labelLink.pack(pady=20)

        # Download Options Frame
        self.frameOptions = customtkinter.CTkFrame(self.frameDownloader, fg_color="transparent")
        self.frameOptions.pack(pady=5)

        self.quality_optionmenu = customtkinter.CTkOptionMenu(self.frameOptions, variable=self.selected_quality, values=["Sélectionner la qualité"], command=self.on_quality_select)
        self.quality_optionmenu.pack(side="left", padx=10)
        self.quality_optionmenu.set("Sélectionner la qualité")

        self.audio_optionmenu = customtkinter.CTkOptionMenu(self.frameOptions, variable=self.selected_audio_format, values=["Non", "Télécharger l'audio"], command=self.on_audio_select)
        self.audio_optionmenu.pack(side="left", padx=10)
        self.audio_optionmenu.set("Non")

        self.download_path_button = customtkinter.CTkButton(self.frameOptions, text="Choisir le dossier", command=self.select_download_path)
        self.download_path_button.pack(side="left", padx=10)

        self.current_download_path_label = customtkinter.CTkLabel(self.frameDownloader, text=f"Dossier de téléchargement: {self.download_path}")
        self.current_download_path_label.pack(pady=5)

        self.labelPercent = customtkinter.CTkLabel(self.frameDownloader, text="0%")
        self.labelPercent.pack()

        self.progressBar = customtkinter.CTkProgressBar(self.frameDownloader, width=500, progress_color="#41A253")
        self.progressBar.set(0)
        self.progressBar.pack()

        # Button frame
        self.frameButtons = customtkinter.CTkFrame(self.frameDownloader, width=520, height=100, fg_color="transparent")
        self.frameButtons.pack(pady=15)

        self.buttonDownload = customtkinter.CTkButton(self.frameButtons, text="Download", corner_radius=30, command=self.onClickDownload, hover_color="#41A253", fg_color="#4180A2")
        self.buttonDownload.pack(side="left", padx=15)

        self.buttonCancel = customtkinter.CTkButton(self.frameButtons, text="Cancel", corner_radius=30, command=self.onClickCancel, hover_color="#CA4A4A", fg_color="#4180A2")
        self.buttonCancel.pack(side="right", padx=15)

        self.finishLabel = customtkinter.CTkLabel(self.frameDownloader, text="", font=("Helvetica", 12, "bold"))
        self.finishLabel.pack()

    def getThumbnail(self, thumbnailLink):
        response = requests.get(thumbnailLink)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize(size=(380, 220))
        return ImageTk.PhotoImage(img)

    def updateIDVideo(self, ytObject):
        self.labelTitre.configure(text="Titre : " + ytObject.title)
        self.labelAuteur.configure(text="Auteur : " + ytObject.author)
        self.labelDuree.configure(text="Duree : " + str(int(round(ytObject.length / 60, 0))) + " min")
        self.labelVues.configure(text="Vues : " + str(round(ytObject.views / 1000, 2)) + " k")
        img = self.getThumbnail(thumbnailLink=ytObject.thumbnail_url)
        self.labelMiniature.configure(image=img)
        self.frameIdentification.update()

        # Populate stream options
        self.available_streams = ytObject.streams
        self.video_qualities = sorted(list(set([s.resolution for s in self.available_streams.filter(progressive=True, file_extension='mp4') if s.resolution])), key=lambda x: int(x[:-1]), reverse=True)
        self.audio_streams = sorted(list(set([s.abr for s in self.available_streams.filter(only_audio=True) if s.abr])), key=lambda x: int(x[:-4]), reverse=True)

        if self.video_qualities:
            self.quality_optionmenu.configure(values=self.video_qualities)
            self.selected_quality.set(self.video_qualities[0])
        else:
            self.quality_optionmenu.configure(values=["Aucune qualité vidéo disponible"])
            self.selected_quality.set("Aucune qualité vidéo disponible")

        if self.audio_streams:
            audio_options = [f"Audio seulement ({abr})" for abr in self.audio_streams]
            self.audio_optionmenu.configure(values=["Non"] + audio_options)
            self.selected_audio_format.set("Non")
        else:
            self.audio_optionmenu.configure(values=["Non"])
            self.selected_audio_format.set("Non")

    def resetIDVideo(self):
        self.labelTitre.configure(text="Titre : ")
        self.labelAuteur.configure(text="Auteur : ")
        self.labelDuree.configure(text="Duree : ")
        self.labelVues.configure(text="Vues : ")
        self.labelMiniature.configure(image=None)
        self.frameIdentification.update()
        self.quality_optionmenu.set("Sélectionner la qualité")
        self.quality_optionmenu.configure(values=["Sélectionner la qualité"])
        self.audio_optionmenu.set("Non")
        self.audio_optionmenu.configure(values=["Non"])
        self.available_streams = []
        self.video_qualities = []
        self.audio_streams = []

    def on_quality_select(self, choice):
        self.selected_quality.set(choice)

    def on_audio_select(self, choice):
        self.selected_audio_format.set(choice)

    def select_download_path(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path = folder_selected
            self.current_download_path_label.configure(text=f"Dossier de téléchargement: {self.download_path}")

    def onClickDownload(self):
        self.flStop = False
        self.finishLabel.configure(text="")
        self.labelPercent.configure(text="0%")
        self.progressBar.set(0)
        self.frameDownloader.update()

        try:
            ytlink = self.labelLink.get()
            # Re-fetch ytObject here to ensure streams are fresh, or store it in self.ytObject after onChangeURL
            # For now, let's assume self.ytObject is correctly set by onChangeURL
            if not self.ytObject or self.ytObject.watch_url != ytlink:
                self.ytObject = YouTube(url=ytlink, on_progress_callback=self.on_progress)
                # Re-run updateIDVideo to populate streams if ytObject changed
                self.updateIDVideo(self.ytObject)

            dlThread = threading.Thread(target=self.download, args=(self.ytObject,))
            dlThread.start()

        except (RegexMatchError, VideoUnavailable):
            self.finishLabel.configure(text="Lien YouTube non valide !", text_color="#CA4A4A")
        except Exception as e:
            if self.flStop:
                self.finishLabel.configure(text="Téléchargement annulé !", text_color="#EA9544")
            else:
                self.finishLabel.configure(text=f"Erreur: {e}", text_color="#CA4A4A")

    def download(self, ytObject):
        sanitized_title = sanitize_filename(ytObject.title)
        download_filepath = ""

        try:
            selected_stream = None
            if self.selected_audio_format.get() != "Non":
                # Download audio only
                abr = self.selected_audio_format.get().replace("Audio seulement (", "").replace(")", "")
                selected_stream = ytObject.streams.filter(only_audio=True, abr=abr).first()
                if selected_stream:
                    file_extension = selected_stream.mime_type.split('/')[-1]
                    download_filepath = os.path.join(self.download_path, f"{sanitized_title}.{file_extension}")
                    selected_stream.download(output_path=self.download_path, filename=sanitized_title + f".{file_extension}")
                else:
                    self.finishLabel.configure(text="Aucun flux audio trouvé pour la sélection !", text_color="#CA4A4A")
                    return
            else:
                # Download video with selected quality
                quality = self.selected_quality.get()
                if quality == "Sélectionner la qualité" or quality == "Aucune qualité vidéo disponible":
                    self.finishLabel.configure(text="Veuillez sélectionner une qualité vidéo !", text_color="#CA4A4A")
                    return

                selected_stream = ytObject.streams.filter(res=quality, progressive=True, file_extension=\'mp4\').first()
                if selected_stream:
                    download_filepath = os.path.join(self.download_path, f"{sanitized_title}.mp4")
                    selected_stream.download(output_path=self.download_path, filename=sanitized_title + ".mp4")
                else:
                    self.finishLabel.configure(text=f"Aucun flux vidéo trouvé pour la qualité {quality}!", text_color="#CA4A4A")
                    return

            if self.flStop:
                if os.path.exists(download_filepath):
                    os.remove(download_filepath)
                self.finishLabel.configure(text="Téléchargement annulé !", text_color="#EA9544")
            else:
                self.finishLabel.configure(text="Téléchargement terminé !", text_color="#41A253")

        except Exception as e:
            if download_filepath and os.path.exists(download_filepath):
                os.remove(download_filepath)
            if self.flStop:
                self.finishLabel.configure(text="Téléchargement annulé !", text_color="#EA9544")
            else:
                self.finishLabel.configure(text=f"Erreur lors du téléchargement: {e}", text_color="#CA4A4A")

    def onClickCancel(self):
        self.flStop = True

    def on_progress(self, stream, chunk, bytes_remaining):
        if self.flStop:
            raise Exception("Téléchargement annulé !")
        total_size = stream.filesize
        bytes_dl = total_size - bytes_remaining
        per_complete = bytes_dl / total_size * 100
        per = str(int(per_complete))
        self.labelPercent.configure(text=per + '%%') # Fixed typo here
        self.labelPercent.update()
        self.progressBar.set(per_complete / 100)

    def onChangeURL(self, *args):
        try:
            ytlink = self.labelLink.get()
            self.ytObject = YouTube(url=ytlink, on_progress_callback=self.on_progress)
            self.updateIDVideo(self.ytObject) # Call updateIDVideo to populate streams
            self.finishLabel.configure(text="") # Clear previous messages on new URL
        except (RegexMatchError, VideoUnavailable):
            self.resetIDVideo()
            self.finishLabel.configure(text="Lien YouTube non valide ou vidéo indisponible !", text_color="#CA4A4A")
        except Exception as e:
            self.resetIDVideo()
            self.finishLabel.configure(text=f"Erreur lors de la récupération des détails: {e}", text_color="#CA4A4A")


if __name__ == "__main__":
    app = customtkinter.CTk()
    yt_app = YTDownloaderApp(app)
    app.mainloop()