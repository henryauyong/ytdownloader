import os
from pytube import YouTube
from pytube.streams import Stream
from pytube import Playlist
import tkinter
from tkinter import ttk
from tkinter import N, W, E, S
from PIL import Image, ImageTk
import requests
from io import BytesIO
import ffmpeg

# video: Video object
# videos: list of Video objects
# videoList: variable for videoListbox
# videoListbox: tk.Listbox
videos = []

class Video:
    def __init__(self, url):
        self.url = url
        try:
            self.yt = YouTube(self.url)
            self.title = self.yt.title
            self.thumbnailUrl = self.yt.thumbnail_url
            self.thumbnail = self.getThumbnail()
            self.availableResolution = []
            availableMp4 = self.yt.streams.filter(file_extension="mp4", type="video")
            for i in availableMp4:
                if int(i.resolution[:-1]) not in self.availableResolution and i.resolution != None:
                    self.availableResolution.append(int(i.resolution[:-1])) # trim of trailing p for sorting
                    self.availableResolution.sort()
        except Exception as e:
            print(e)
            self.yt = None
            self.title = "[invalid video]"
            self.thumbnailUrl = None
            self.availableResolution = None
            availableMp4 = None
            self.stream = None
    def searchStream():
        pass
    def getThumbnail(self):
        imgResponse = requests.get(self.thumbnailUrl)
        resizedThumbnail = Image.open(BytesIO(imgResponse.content)).resize((450, 350), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resizedThumbnail)

# download the whole list of videos
def download():
    global status
    for video in videos:
        audio = video.yt.streams.filter(type="audio")[0]
        if(downloadFormat.get() == "video"):
            res = 720 # default
            for i in resolutionList:
                if int(i[:-1]) <= int(str(resolutionListvar.get())[:-1]) and int(i[:-1]) in video.availableResolution:
                    res = int(i[:-1])
                    break
            stream = video.yt.streams.filter(resolution=str(res) + "p", file_extension="mp4")[0]

            if(res >= 1080):
                try:
                    stream.download(output_path='video', filename='tempVideo.mp4')
                    audio.download(output_path='video', filename='tempAudio.mp4')
                    input_video = ffmpeg.input('video/tempVideo.mp4')
                    input_audio = ffmpeg.input('video/tempAudio.mp4')
                    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(filename="./video/"+str(video.title)+".mp4").run()
                    os.remove('./video/tempVideo.mp4')
                    os.remove('./video/tempAudio.mp4') 
                except Exception as e:
                    print(e)
            else:
                try:
                    stream.download(output_path='video')
                except Exception as e:
                    print(e)
        else:
            try:
                audio.download(output_path='video')
            except Exception as e:
                print(e)
    status.config(text="Download completed! check video/")

def addEntry():
    global inputname, status, urlVar, videoList, frame
    status.config(text="Adding video...")
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
    inputname.delete(0, tkinter.END) # clear input field
    status.config(text="Done")

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
    global frame, inputname, status, urlVar, videoList, videoListvar, videoListbox, thumbnailLabel, resolutionListvar, resolutionList, downloadFormat

    # window configuration
    window = tkinter.Tk()
    window.title("YouTube Downloader")

    frame = ttk.Frame(window, borderwidth=2, relief="sunken")
    editFrame = ttk.Frame(frame, borderwidth=2, relief="sunken")
    optionFrame = ttk.Frame(frame, borderwidth=2, relief="sunken")

    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    editFrame.grid(column=4, row=1, sticky=(N, E, W))
    optionFrame.grid(column=4, row=2, sticky=(N, W, E, S))

    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # widgets configuration
    # "Enter URL:"
    ttk.Label(frame, text="Enter URL: ").grid(column=0, row=0)

    # input url
    urlVar = tkinter.StringVar()
    inputname = tkinter.Entry(frame, textvariable=urlVar)
    inputname.focus()

    # list and scrollbar
    videoList = []
    videoListvar = tkinter.StringVar(value=videoList)
    videoListbox = tkinter.Listbox(frame, listvariable=videoListvar)
    scrollbar = ttk.Scrollbar(frame, orient=tkinter.VERTICAL, command=videoListbox.yview)
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

    # dropdown manu for resolution and format choices
    resolutionList = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
    resolutionListvar = tkinter.StringVar(value="720p")
    resolutionListoption = tkinter.OptionMenu(optionFrame, resolutionListvar, *resolutionList)

    # radiobutton for choosing download download format
    downloadFormat = tkinter.StringVar(value="video")
    videoButton = tkinter.Radiobutton(optionFrame, text="Video", variable=downloadFormat, value="video")
    audioButton = tkinter.Radiobutton(optionFrame, text="Audio", variable=downloadFormat, value="audio")

    # widgets grid configuration
    inputname.grid(column=1, row=0, sticky=(W, E))
    videoListbox.grid(column=0, row=1, rowspan=2, columnspan=3, sticky=(N, E, S, W))
    scrollbar.grid(column=3, row=1, rowspan=2, sticky=(N, S, W))
    inputbutton.grid(column=2, row=0, sticky=(W))
    removebutton.grid(column=3, row=0, sticky=())
    status.grid(column=0, row=3)
    downloadButton.grid(column=4, row=3)
    thumbnailLabel.grid(column=0, row=0)
    resolutionListoption.grid(column=0, row=0)
    videoButton.grid(column=1, row=0)
    audioButton.grid(column=1, row=1)

    # frame configuration
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    window.mainloop()

if __name__ == "__main__":
    main()