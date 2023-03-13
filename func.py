import os
from pytube import Search
from pytube import YouTube
import moviepy.editor as me
import sys

def download_videos(x, n, d):
    d=int(d)
    n=int(n)
    if not os.path.exists(f"static/{x}"):
        os.mkdir(f"static/{x}")

    pathh=f"static/{x}"
    query = x + " music videos"
    s = Search(query)
    # searchResults = {}
    i = 0
    for v in s.results:
        if i < n:
            if(v.length<300):
                # searchResults[v.title] = v.watch_url
                youtubeObject = YouTube(v.watch_url)
                try:
                    youtubeObject = youtubeObject.streams.get_highest_resolution().download(pathh,filename=f"{i}.mp4")
                    print(f"Downloaded video {i + 1}: {v.title}")
                    i = i+1
                except:
                    print("error")

    for k in range(0,n):
        try:
            clip=me.VideoFileClip(f"{pathh}/{k}.mp4").subclip(0,d)
            clip.audio.write_audiofile(f"{pathh}/{k}.mp3")
        except:
            sys.exit(0)

    audio_files=[me.AudioFileClip(f"static/{x}/{k}.mp3") for k in range(0,n)]
    res=me.concatenate_audioclips(audio_files)
    res.write_audiofile(f"static/{x}/mashup.mp3")
    


# n = int(input("Enter the number of videos to download: "))
# x = input("Enter the name of the singer: ")
# d = input("Enter duration of each video")
# output = input("Enter name of output file")
# download_videos(x, n, d)
# download_videos(2, "Taylor Swift")