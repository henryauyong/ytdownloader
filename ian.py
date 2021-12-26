from pytube import YouTube
from pytube.streams import Stream

inputname = str(input())
yt = YouTube(inputname)

availableMp4 = yt.streams.filter(file_extension='mp4', type="video")
print("mp4: ")
for i in availableMp4:
    print(i)

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