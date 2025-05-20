from pytube import YouTube
from pytube import Playlist
from playsound import playsound
from win10toast import ToastNotifier
import datetime as dt
import eyed3
import json
import requests
import sys
import os

# default
download_dir =  os.path.join(os.path.expanduser('~'), 'downloads', 'MP3 Youtube Downloader')
mute = False
notif = True
start_file = 0
current_file = '#'

def setup():
    try:
        global mute 
        global download_dir
        with open('settings.json', 'r') as file:
            settings = json.load(file)
        mute = settings['mute']
        notif = settings['notif']
        if settings['dir'] == 'default':
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
        else:
            download_dir = settings['dir']
    except Exception as e:
        print(f"[#] Error: {str(e)}")
        with open('settings.json', 'w') as file:
            download_dir = 'default'
        save()

def save():
    data = {
        "dir": str(download_dir),
        "mute": mute,
        "notif": notif
    }
    with open("settings.json", 'w') as file:
        json.dump(data, file)

def help():
    print(
"""usage: mp3yt -v [video url]     : download mp3 from video link
             -vt [video url]    : download mp3 from video link with author
             -p [playlist url]  : download mp3 from playlist link
             -pt [playlist url] : download mp3 from playlist link with author
             dir                : show current download directory
             cd [directory]     : change download directory
             help               : show help
NOTES: video or playlist must be public or unlisted.""")

def log_write(url, title, duration):
    with open('log.txt', 'a') as log_file:
        x = dt.datetime.now()
        log_file.write(f"[{x.strftime("%y/%m/%d %H:%M")}] URL: {url}, title:{title} {duration}\n")
        
def end_download(hidden = 0):
    if hidden:
        print(f"Some files are hidden or removed.")
    print(f"The downloaded file is located in the directory: {os.path.join(download_dir)}")
    if not mute:
        playsound("sound/playsound.wav")
    if notif:
        ToastNotifier().show_toast("Succesfuly Download", f"The downloaded file is located in the directory: {os.path.join(download_dir)}", duration=5)
    save()
    
def download_audio(url, bool_author, len_playlist = 0):
    try:
        if len_playlist:
            global start_file
            global current_file
            start_file += 1
            current_file = f"{start_file}/{len_playlist}"
            
        print(f"[{current_file}] Get data..", end='\r')
        yt = YouTube(url)
        if bool_author:
            title = f"{yt.author} - {yt.title.replace('|', '').replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('"', '').replace('*', '').replace('<', '').replace('>', '')}"
        else:
            title = f"{yt.title.replace('|', '').replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('"', '').replace('*', '').replace('<', '').replace('>', '')}"
        duration = f"{yt.length//60}m {yt.length%60}s"
        print(f"[{current_file}] Downloading: {title} ({duration})", end='\r')
        audio = yt.streams.filter(only_audio=True).first()
        temp_file = audio.download(output_path=os.path.join(download_dir), filename="temp_audio")
        new_file = os.path.join(download_dir, title + '.mp3')
        
        if os.path.exists(os.path.join(download_dir, title + '.mp3')):
            i = 1
            while True:
                new_file = os.path.join(download_dir, f"{title} ({i}).mp3")
                if not os.path.exists(new_file):
                    title = f"{title} ({i})"
                    break
                i += 1
        os.rename(temp_file, new_file)
        print(f"[{current_file}] Success download: {title} ({duration})")
        
        log_write(url, title, duration)

        response = requests.get(yt.thumbnail_url)
        with open(os.path.join(download_dir, 'thumb.jpg'), 'wb') as f:
            f.write(response.content)
        audiofile = eyed3.load(os.path.join(download_dir, title + '.mp3'))
        if audiofile.tag is None:
            audiofile.initTag()
        with open(os.path.join(download_dir, 'thumb.jpg'), 'rb') as f:
            thumbnail_data = f.read()
        audiofile.tag.images.set(3, thumbnail_data, "image/jpeg", u"Thumbnail")
        audiofile.tag.save()
        os.remove(os.path.join(download_dir, 'thumb.jpg'))
        
        if (current_file == len_playlist) or (len_playlist == 0):
            return 0
        else:
            return 1
        
    except Exception as e:
        print(f"[{current_file}] Error: {str(e)}")
        return 0

if __name__ == "__main__":
    try:
        setup()
        if len(sys.argv) > 1:
            if(sys.argv[1] == '-v'):
                download_audio(sys.argv[2], False)
                end_download()

            elif(sys.argv[1] == '-vt'):
                download_audio(sys.argv[2], True)
                end_download()
                
            elif(sys.argv[1] == '-p'):
                playlist = Playlist(sys.argv[2])
                duration_playlist = 0
                print(f"[#] Get data..", end='\r')
                for video_url in playlist.video_urls:
                    duration_playlist += YouTube(video_url).length
                print(f"[#] Title Playlist: {playlist.title} ({playlist.owner}) ({playlist.length} videos) ({duration_playlist//60}m {duration_playlist%60}s)")
                for video_url in playlist.video_urls:
                    hidden = download_audio(video_url, False, playlist.length)
                end_download(hidden)

            elif(sys.argv[1] == '-pt'):
                playlist = Playlist(sys.argv[2])
                duration_playlist = 0
                print(f"[#] Get data..", end='\r')
                for video_url in playlist.video_urls:
                    duration_playlist += YouTube(video_url).length
                print(f"[#] Title Playlist: {playlist.title} ({playlist.owner}) ({playlist.length} videos) ({duration_playlist//60}m {duration_playlist%60}s)")
                for video_url in playlist.video_urls:
                    hidden = download_audio(video_url, True, playlist.length)
                end_download(hidden)

            elif(sys.argv[1] == 'dir'):
                print(f"Download directory: {download_dir}")
                
            elif(sys.argv[1] == 'cdir'):
                download_dir = sys.argv[2]
                print("Successfully changed the download folder direction")
                
            elif(sys.argv[1] == "help"):
                help()
                
            else:
                print("Wrong input")
                help()
        else:
            print("mp3yt 1.1.3 by Fawwas Aliy (FechL) [https://github.com/FechL/mp3yt]\nSimple tool that allows users to quickly and easily download YouTube videos in MP3 format.")
            help()
            
    except Exception as e:
        print(f"[#] Error: {str(e)}")

