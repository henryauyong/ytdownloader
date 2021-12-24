# download button will default to download mp4 at 720p
from os import remove
from pytube import YouTube
from pytube.streams import Stream
from pytube import Playlist
import tkinter
from tkinter import ttk
from tkinter import *
from PIL import Image
import requests
from io import BytesIO

yt = None

def searchStream():
    global inputname, yt, status, url, choices, frame
    status.config(text = "searching for stream...")

    print(url.get())
    try:
        yt = YouTube(url.get())
    except Exception as e:
        status.config(text = "Cannot find video")
        return
    
    if "&list=" in url.get():
        playlist = Playlist(url.get())
        print("It's a playlist")
        for playlisturl in playlist.video_urls:
            choices.append(YouTube(playlisturl).title)
            choicesvar.set(choices)
    else:
        choices.append(yt.title)
        choicesvar.set(choices)
        inputname.delete(0, END)

    availableMp4 = yt.streams.filter(file_extension='mp4', type="video")
    print("mp4: ")
    for i in range(len(availableMp4)):
        if(availableMp4[i - 1].resolution != availableMp4[i].resolution):
            print(availableMp4[i].resolution)

    availableMp3 = yt.streams.filter(type='audio')
    print("mp3: ")
    for i in range(len(availableMp3)):
        print(availableMp3[i])


    #download("mp4", "720p")
    

def download(format, resolution=None):
    global status
    if(format == 'mp4'):
        try:
            stream = yt.streams.filter(res=resolution)[0]
            print(stream)
            stream.download(output_path='Python/video')
            status.config(text = "download completed! check Python/video/")
        except Exception as e:
            print(e)
    if(format == 'mp3'):
        try:
            stream = yt.streams.filter(type='audio')[0]
            print(stream)
            stream.download(output_path='Python/video')
            status.config(text = "download completed! check Python/video/")
        except Exception as e:
            print(e)

def removeEntry(*args):
    if len(choices) > 0:
        selection = choiceslist.curselection()
        choices.pop(selection[0])
        choicesvar.set(choices)

def openEdit(*args):
    selection = choiceslist.curselection()
    print(selection[0])

def test(*args):
    print("Hello")

def main():
    global inputname, status, url, choices, frame, choicesvar, choiceslist, inputname

    # window configuration
    window = tkinter.Tk()
    window.title("YouTube Downloader")
    frame = ttk.Frame(window, borderwidth=2, relief="sunken")
    editFrame = ttk.Frame(frame, borderwidth=2, relief="sunken")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    editFrame.grid(column=4, row=1, sticky=(N, E, S, W))
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # widgets configuration
    url = StringVar()
    choices = []
    ttk.Label(frame, text="Enter URL: ").grid(column=0, row=0)
    inputname = tkinter.Entry(frame, textvariable=url)
    inputname.focus()
    choicesvar = StringVar(value=choices)
    choiceslist = Listbox(frame, listvariable=choicesvar)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=choiceslist.yview)
    choiceslist.config(yscrollcommand=scrollbar.set)
    inputbutton = tkinter.Button(frame, text="Add", command=searchStream)
    removebutton = tkinter.Button(frame, text="Remove", command=removeEntry)
    status = tkinter.Label(frame, text="")

    inputname.grid(column=1, row=0, sticky=(W, E))
    choiceslist.grid(column=0, row=1, columnspan=3, sticky=(N, E, S, W))
    scrollbar.grid(column=3, row=1, sticky=(N, S, W))
    inputbutton.grid(column=2, row=0, sticky=(W))
    removebutton.grid(column=3, row=0, sticky=())
    status.grid(column=0, row=2)

    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(4, weight=1)

    frame.rowconfigure(1, weight=1)

    choiceslist.bind("<<ListboxSelect>>", openEdit)

    window.mainloop()

if __name__ == "__main__":
    main()