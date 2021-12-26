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
# videoList: variable for videoListbox
# videoListbox: tk.Listbox
videos = []

# todo
# considering making resolution and format argument of download()
# add thumbnail preview

class Video:
    # url is a string here (sadly)
    def __init__(self, url):
        global status
        status.config(text="Searching for video...")
        self.url = url
        try:
            self.yt = YouTube(self.url)
            self.title = self.yt.title
            self.thumbnailUrl = self.yt.thumbnail_url
            self.thumbnail = self.getThumbnail()
            self.format = "mp4"
            self.availableResolution = []
            availableMp4 = self.yt.streams.filter(file_extension="mp4", type="video")
            for i in availableMp4:
                if i.resolution not in self.availableResolution:
                    self.availableResolution.append(int(i.resolution[:-1])) # trim of trailing p for sorting
                    self.availableResolution.sort()
            self.resolution = str(self.availableResolution[-1]) + "p"
            self.stream = self.yt.streams.filter(resolution=self.resolution, file_extension=self.format)[0]
        except Exception as e:
            print(e)
            self.yt = None
            self.title = "[invalid video]"
            self.thumbnailUrl = None
            self.format = None
            self.resolution = None
            self.availableResolution = None
            availableMp4 = None
            self.stream = None
        status.config(text="Done")
    def findStream():
        pass
    def getThumbnail(self):
        imgResponse = requests.get(self.thumbnailUrl)
        resizedThumbnail = Image.open(BytesIO(imgResponse.content)).resize((450, 350), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resizedThumbnail)

# download the whole list of videos
def download():
    global status
    for video in videos:
        try:
            stream = video.stream
            stream.download(output_path='video')
        except Exception as e:
            print(e)
    status.config(text="Download completed! check video/")

def addEntry():
    global inputname, yt, status, urlVar, videoList, frame
    url = urlVar.get()
    # check if url is a playlist
    # could be &list=... or ?list=...
    if "list=" in url:
        playlist = Playlist(url)
        for videoUrl in playlist.video_urls:
            video = Video(videoUrl)
            videos.append(video)
            videoList.append(video.title)
    # if url is a video
    else:
        video = Video(url)
        videos.append(video)
        videoList.append(video.title)

    videoListvar.set(videoList)
    inputname.delete(0, END)

def removeEntry(*args):
    if len(videoList) > 0:
        selection = videoListbox.curselection()[0]
        videoList.pop(selection)
        videos.pop(selection)
        videoListvar.set(videoList)

def openEdit(*args):
    global thumbnailLabel
    selection = videoListbox.curselection()[0] # index of current selection
    thumbnailLabel['image'] = videos[selection].thumbnail
    thumbnailLabel.image = videos[selection].thumbnail

def main():
    global inputname, status, urlVar, videoList, frame, videoListvar, videoListbox, inputname, thumbnailLabel

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
    urlVar = StringVar()
    inputname = tkinter.Entry(frame, textvariable=urlVar)
    inputname.focus()

    # list and scrollbar
    videoList = []
    videoListvar = StringVar(value=videoList)
    videoListbox = Listbox(frame, listvariable=videoListvar)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=videoListbox.yview)
    videoListbox.config(yscrollcommand=scrollbar.set)
    videoListbox.bind("<<ListboxSelect>>", openEdit)

    # add and remove button
    inputbutton = tkinter.Button(frame, text="Add", command=addEntry)
    removebutton = tkinter.Button(frame, text="Remove", command=removeEntry)
    status = tkinter.Label(frame, text="")

    # download button
    downloadButton = tkinter.Button(frame, text="Download", command=download)

    # thumbnail label
    thumbnailLabel = tkinter.Label(editFrame, text="Please select a video",image="")

    # widgets grid configuration
    inputname.grid(column=1, row=0, sticky=(W, E))
    videoListbox.grid(column=0, row=1, columnspan=3, sticky=(N, E, S, W))
    scrollbar.grid(column=3, row=1, sticky=(N, S, W))
    inputbutton.grid(column=2, row=0, sticky=(W))
    removebutton.grid(column=3, row=0, sticky=())
    status.grid(column=0, row=2)
    downloadButton.grid(column=4, row=2)
    thumbnailLabel.grid(column=0, row=0, columnspan=2)

    # frame configuration
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(4, weight=1)
    frame.rowconfigure(1, weight=1)
    editFrame.columnconfigure(0, weight=1)

    window.mainloop()

if __name__ == "__main__":
    main()