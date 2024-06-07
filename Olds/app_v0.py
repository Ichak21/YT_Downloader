import threading
import tkinter
import os
import customtkinter
from pytube import YouTube
import requests
from PIL import Image, ImageTk
from io import BytesIO


def getThumbnail(thumbnailLink):
    response = requests.get(thumbnailLink)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize(size=(380,220))
    return ImageTk.PhotoImage(img)

def updateIDVideo(ytObject):
    labelTitre.configure(text="Titre : " + ytObject.title)
    labelAuteur.configure(text="Auteur : " + ytObject.author)
    labelDuree.configure(text="Duree : " + str(int(round(ytObject.length/60,0))) + " min")
    labelVues.configure(text="Vues : " + str(round(ytObject.views/1000,2)) + " k")
    img = getThumbnail(thumbnailLink=ytObject.thumbnail_url)
    labelMiniature.configure(image=img)
    frameIdentification.update()

def resetIDVideo():
    labelTitre.configure(text="Titre : ")
    labelAuteur.configure(text="Auteur : ")
    labelDuree.configure(text="Duree : ")
    labelVues.configure(text="Vues : ")
    labelMiniature.configure(image=None)
    frameIdentification.update()

def onClickDownload():
    try:
        ytlink = labelLink.get()
        ytObject = YouTube(url=ytlink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        video.download()
        finishLabel.configure(text="Download is done !", text_color="#41A253")
    except:
        finishLabel.configure(text="Youtube link is not valid !", text_color="#CA4A4A")

def onClickCancel():
    print("cancel")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_dl = total_size-bytes_remaining
    per_complete = bytes_dl / total_size * 100
    per = str(int(per_complete))
    labelPercent.configure(text = per + '%')
    labelPercent.update()
    progressBar.set(per_complete/100)

def onChangeURL(*args):
    try:
        ytObject = YouTube(url=labelLink.get())
        updateIDVideo(ytObject)
    except:
        resetIDVideo()



# System setting
customtkinter.set_appearance_mode("System")

# Main Window
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YT Downloader +")


#Frame identification video
frameIdentification = customtkinter.CTkFrame(app, width=700, height=240)
frameIdentification.pack(fill="both", side="top", pady=10, padx=10)

labelMiniature = customtkinter.CTkLabel(frameIdentification, width=380, height=220,fg_color="transparent", text=None)
labelMiniature.pack(side="left", padx=10, pady=10)


#Sub Frame for details of video
frameDetails = customtkinter.CTkFrame(frameIdentification, width=300, height=240)
frameDetails.pack(fill="both", padx=10, pady=10,expand=True, anchor="n")

labelTitre = customtkinter.CTkLabel(frameDetails, text="Titre : ", anchor="w" , wraplength=290, font=("Helvetica", 12, "bold"))
labelTitre.pack(padx=10,fill="both",side="top",expand=True)

labelAuteur = customtkinter.CTkLabel(frameDetails, text="Auteur : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
labelAuteur.pack(padx=10,fill="both",side="top",expand=True)

labelDuree = customtkinter.CTkLabel(frameDetails, text="Duree : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
labelDuree.pack(padx=10,fill="both",side="top",expand=True)

labelVues = customtkinter.CTkLabel(frameDetails, text="Vues : ", anchor="w", wraplength=290, font=("Helvetica", 12, "bold"))
labelVues.pack(padx=10,fill="both",side="top",expand=True)


#Frame de control pour download
frameDownloader = customtkinter.CTkFrame(app, width=700, height=220, fg_color="transparent")
frameDownloader.pack()

urlValue = tkinter.StringVar()
urlValue.trace("w", onChangeURL)
labelLink = customtkinter.CTkEntry(frameDownloader, textvariable=urlValue, corner_radius=10, width=400, height=40, border_color="#4180A2")
labelLink.pack(pady=20)

labelPercent = customtkinter.CTkLabel(frameDownloader, text="0%")
labelPercent.pack()

progressBar = customtkinter.CTkProgressBar(frameDownloader, width=500, progress_color="#41A253")
progressBar.set(0)
progressBar.pack()


# Button frame
frameButtons = customtkinter.CTkFrame(frameDownloader, width=520, height=100, fg_color="transparent")
frameButtons.pack(pady=15)

buttonDownload = customtkinter.CTkButton(frameButtons, text="Download",corner_radius=30, command=onClickDownload, hover_color="#41A253", fg_color="#4180A2")
buttonDownload.pack(side="left", padx = 15)

buttonCancel = customtkinter.CTkButton(frameButtons, text="Cancel",corner_radius=30, command=onClickCancel, hover_color="#CA4A4A", fg_color="#4180A2")
buttonCancel.pack(side="right", padx = 15)

finishLabel = customtkinter.CTkLabel(frameDownloader, text="", font=("Helvetica", 12, "bold"))
finishLabel.pack()

# Run app
app.mainloop()