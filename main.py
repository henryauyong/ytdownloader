from pytube import YouTube
from pytube.streams import Stream
from tkinter import *
from tkinter import ttk
import os
import requests
from io import BytesIO

root = Tk() ## Create the main window
root.title("YTDownloader")

mainframe = ttk.Frame(root, borderwidth = 2, relief = "sunken")
mainframe.grid(column = 0, row = 0, sticky=(N, W, E, S))

url = StringVar() ## Entry for URL
url_entry = ttk.Entry(mainframe, width = 30, textvariable = url)
url_entry.grid(column = 0, row = 0, sticky=(W, E))

def getVideo(url):
    try:
        global yt
        yt = YouTube(url)
    except Exception as e:
        pass

add_button = ttk.Button(mainframe, text = "Add", command = getVideo(url))
add_button.grid(column = 1, row = 0, sticky=(W))

thumbnail_url = yt.thumbnail_url
response = requests.get(thumbnail_url)
thumbnail = Image.open(BytesIO(response.content))
preview = ttk.Label(mainframe, text = url, image = thumbnail)

availableMp4 = yt.streams.filter(file_extension='mp4', type="video")
print("mp4: ")
for i in range(len(availableMp4)):
    if(availableMp4[i - 1].resolution != availableMp4[i].resolution):
        print(availableMp4[i].resolution)

availableMp3 = yt.streams.filter(type='audio')
print("mp3: ")
for i in range(len(availableMp3)):
    print(availableMp3[i])
inputtype = str(input("mp4/mp3: "))

if(inputtype == 'mp4'):
    inputres = str(input("resolution: "))
    try:
        stream = yt.streams.filter(res=inputres)[0]
        print(stream)
        stream.download(output_path='Python/video')
    except Exception as e:
        print(e)

if(inputtype == 'mp3'):
    try:
        stream = yt.streams.filter(type='audio')[0]
        print(stream)
        stream.download(output_path='Python/video')
    except Exception as e:
        print(e)