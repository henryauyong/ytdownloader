# download button will default to download mp4 at 720p
from os import remove
from pytube import YouTube
from pytube.streams import Stream
from pytube import Playlist
import tkinter
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

yt = None
videoAttributes = {'title':"", 'thumbnailUrl':""}
videos = []

def searchStream():
    global inputname, yt, status, url, choices, frame
    status.config(text = "searching for stream...")

    try:
        yt = YouTube(url.get())
    except Exception as e:
        status.config(text = "Invalid url")
        inputname.delete(0, END)
        return
    
    # check if it is a playlist
    if "&list=" in url.get():
        playlist = Playlist(url.get())
        for playlisturl in playlist.video_urls:
            videoAttributes['title'] = YouTube(playlisturl).title
            videoAttributes['thumbnailUrl'] = YouTube(playlisturl).thumbnail_url
            videos.append(videoAttributes)
            choices.append(videoAttributes['title'])
            choicesvar.set(choices)
            inputname.delete(0, END)
    # if not
    else:
        videoAttributes['title'] = yt.title
        videoAttributes['thumbnailUrl'] = yt.thumbnail_url
        videos.append(videoAttributes)
        choices.append(videoAttributes['title'])
        choicesvar.set(choices)
        inputname.delete(0, END)

"""
    availableMp4 = yt.streams.filter(file_extension='mp4', type="video")
    print("mp4: ")
    for i in range(len(availableMp4)):
        if(availableMp4[i - 1].resolution != availableMp4[i].resolution):
            print(availableMp4[i].resolution)

    availableMp3 = yt.streams.filter(type='audio')
    print("mp3: ")
    for i in range(len(availableMp3)):
        print(availableMp3[i])
"""

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

"""
    selectedVideo = (videos[selection[0]])['thumbnailUrl'])
    response = requests.get(selectedVideo)
    img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
    thumbnail['image'] = img
    thumbnail.image = img
"""

def test(*args):
    print("Hello")

def main():
    global inputname, status, url, choices, frame, choicesvar, choiceslist, inputname, thumbnail

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
    # "Enter URL:"
    ttk.Label(frame, text="Enter URL: ").grid(column=0, row=0)

    # input url
    url = StringVar()
    inputname = tkinter.Entry(frame, textvariable=url)
    inputname.focus()

    # list and scrollbar
    choices = []
    choicesvar = StringVar(value=choices)
    choiceslist = Listbox(frame, listvariable=choicesvar)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=choiceslist.yview)
    choiceslist.config(yscrollcommand=scrollbar.set)
    choiceslist.bind("<<ListboxSelect>>", openEdit)

    # add and remove button
    inputbutton = tkinter.Button(frame, text="Add", command=searchStream)
    removebutton = tkinter.Button(frame, text="Remove", command=removeEntry)
    status = tkinter.Label(frame, text="")

    # thumbnail
    thumbnail = tkinter.Label(editFrame, text="Please select a video",image="")

    # widgets grid configuration
    inputname.grid(column=1, row=0, sticky=(W, E))
    choiceslist.grid(column=0, row=1, columnspan=3, sticky=(N, E, S, W))
    scrollbar.grid(column=3, row=1, sticky=(N, S, W))
    inputbutton.grid(column=2, row=0, sticky=(W))
    removebutton.grid(column=3, row=0, sticky=())
    status.grid(column=0, row=2)
    thumbnail.grid(column=0, row=0)

    # frame configuration
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(4, weight=1)
    frame.rowconfigure(1, weight=1)

    window.mainloop()

if __name__ == "__main__":
    main()