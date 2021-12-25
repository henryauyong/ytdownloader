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

# video: Video object
# videos: list of Video objects
# videoList: ?
# videoListlist: tk.Listbox
videos = []

# todo
# considering making resolution and format argument of download()
# add thumbnail preview

class Video:
    # url is a string here (sadly)
    def __init__(self, url):
        self.url = url
        try:
            self.yt = YouTube(self.url)
            self.title = self.yt.title
            self.thumbnail_url = self.yt.thumbnail_url
            self.format = "mp4"
            self.resolution = "720p"
            # thumbnail url
        except Exception as e:
            print(e)
            self.yt = None
            self.title = "[invalid video]"
            self.thumbnail_url = None
            self.format = None
            self.resolution = None

def searchStream():
    global inputname, yt, status, url, videoList, frame
    status.config(text = "searching for stream...")

    try:
        yt = YouTube(url.get())
    except Exception as e:
        status.config(text = "Invalid url")
        inputname.delete(0, END)
        return

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
    

# download the whole list of vids
def download():
    global videoList, status
    for video in videos:
        if(video.format == 'mp4'):
            try:
                stream = yt.streams.filter(res=video.resolution)[0]
                #print(stream)
                stream.download(output_path='video')
                status.config(text = "download completed! check video/")
            except Exception as e:
                print(e)
        if(video.format == 'mp3'):
            try:
                stream = yt.streams.filter(type='audio')[0]
                print(stream)
                stream.download(output_path='video')
                status.config(text = "download completed! check video/")
            except Exception as e:
                print(e)

def addEntry():
    global inputname, yt, status, url, videoList, frame
    # check if url is a playlist
    if "&list=" in url.get():
        playlist = Playlist(url.get())
        for playlisturl in playlist.video_urls:
            video = Video(playlisturl)
            videos.append(video)
            videoList.append(video.title)
            videoListvar.set(videoList)
            inputname.delete(0, END)
    # if url is a video
    else:
        video = Video(url.get())
        videos.append(video)
        videoList.append(video.title)
        videoListvar.set(videoList)
        inputname.delete(0, END)

def removeEntry(*args):
    if len(videoList) > 0:
        selection = videoListlist.curselection()
        videoList.pop(selection[0])
        videos.pop(selection[0])
        videoListvar.set(videoList)

def openEdit(*args):
    global thumbnail
    selection = videoListlist.curselection()
    thumbnailUrl = videos[selection[0]].thumbnail_url
    response = requests.get(thumbnailUrl)
    img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
    thumbnail['image'] = img
    thumbnail.image = img


def main():
    global inputname, status, url, videoList, frame, videoListvar, videoListlist, inputname, thumbnail

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
    videoList = []
    videoListvar = StringVar(value=videoList)
    videoListlist = Listbox(frame, listvariable=videoListvar)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=videoListlist.yview)
    videoListlist.config(yscrollcommand=scrollbar.set)
    videoListlist.bind("<<ListboxSelect>>", openEdit)

    # add and remove button
    inputbutton = tkinter.Button(frame, text="Add", command=addEntry)
    removebutton = tkinter.Button(frame, text="Remove", command=removeEntry)
    status = tkinter.Label(frame, text="")

    # download button
    #downloadButton = tkinter.Button(frame, text="Download", commmand=download)

    # thumbnail
    thumbnail = tkinter.Label(editFrame, text="Please select a video",image="")

    # widgets grid configuration
    inputname.grid(column=1, row=0, sticky=(W, E))
    videoListlist.grid(column=0, row=1, columnspan=3, sticky=(N, E, S, W))
    scrollbar.grid(column=3, row=1, sticky=(N, S, W))
    inputbutton.grid(column=2, row=0, sticky=(W))
    removebutton.grid(column=3, row=0, sticky=())
    status.grid(column=0, row=2)
    #downloadButton.grid(column=4, row=2)
    thumbnail.grid(column=0, row=0)

    # frame configuration
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(4, weight=1)
    frame.rowconfigure(1, weight=1)

    window.mainloop()

if __name__ == "__main__":
    main()