from pytube import YouTube
from pytube import Playlist
import datetime as dt
import sys
import os

def help():
    print(
"""usage: mp3yt -v [video url]     : download mp3 from video link
             -vt [video url]    : download mp3 from video link with author
             -p [playlist url]  : download mp3 from playlist link
             -pt [playlist url] : download mp3 from playlist link with author
             dir                : show current download directory
             cd [directory]     : change download directory
             help               : show help""")
    
download_dir = os.path.join(os.path.expanduser('~'), 'downloads', 'MP3 Youtube Downloader')

def download_audio(url, bool_author):
    try:
        print(f"[#] Get data..", end='\r')
        yt = YouTube(url)
        if bool_author:
            title = f"{yt.author} - {yt.title.replace('|', '').replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('"', '').replace('*', '').replace('<', '').replace('>', '')}"
        else:
            title = f"{yt.title.replace('|', '').replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('"', '').replace('*', '').replace('<', '').replace('>', '')}"
        duration = f"{yt.length//60}m {yt.length%60}s"
        print(f"[#] Downloading: {title} ({duration})", end='\r')
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
        print(f"[#] Success download: {title} ({duration})")
        with open(os.path.join(download_dir, 'log.txt'), 'a') as log_file:
            x = dt.datetime.now()
            log_file.write(f"[{x.strftime("%y/%m/%d %H:%M")}] URL: {url}, title:{title}\n")
    except Exception as e:
        print(f"[#] Error: {str(e)}")

if __name__ == "__main__":
    try:
        with open("dir.txt", 'r') as file:
            first_char = file.read(1)
            if not first_char:
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
            else:
                download_dir = file.readline().strip()
    except Exception as e:
        print(f"[#] Error: {str(e)}")
        with open("dir.txt", 'w') as file:
            file.write("")
    try:
        if len(sys.argv) > 1:
            if(sys.argv[1] == '-v'):
                download_audio(sys.argv[2], False)
                print(f"The downloaded file is located in the directory: {os.path.join(download_dir)}")
            elif(sys.argv[1] == '-vt'):
                download_audio(sys.argv[2], True)
                print(f"The downloaded file is located in the directory: {os.path.join(download_dir)}")
            elif(sys.argv[1] == '-p'):
                playlist = Playlist(sys.argv[2])
                duration_playlist = 0
                for video_url in playlist.video_urls:
                    duration_playlist += YouTube(video_url).length
                print(f"[#] Title Playlist: {playlist.title} ({playlist.owner}) ({playlist.length} videos) ({duration_playlist//60}m {duration_playlist%60}s)")
                for video_url in playlist.video_urls:
                    download_audio(video_url, False)
                print(f"The downloaded file is located in the directory: {os.path.join(download_dir)}")
            elif(sys.argv[1] == '-pt'):
                playlist = Playlist(sys.argv[2])
                duration_playlist = 0
                for video_url in playlist.video_urls:
                    duration_playlist += YouTube(video_url).length
                print(f"[#] Title Playlist: {playlist.title} ({playlist.owner}) ({playlist.length} videos) ({duration_playlist//60}m {duration_playlist%60}s)")
                for video_url in playlist.video_urls:
                    download_audio(video_url, True)
                print(f"The downloaded file is located in the directory: {os.path.join(download_dir)}")
            elif(sys.argv[1] == 'dir'):
                print(f"Download directory: {download_dir}")
            elif(sys.argv[1] == 'cd'):
                with open(os.path.join(sys.argv[2], 'log.txt'), 'a') as file:
                    file.write('')
                with open("dir.txt", 'w') as file:
                    file.write('"' + sys.argv[2])
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

