from pytube import YouTube
import datetime as dt
import sys
import os

download_dir = os.path.join(os.path.expanduser('~'), 'downloads')

def download_audio(url):
    try:
        print(f"[#] Get data from youtube", end='\r')
        yt = YouTube(url)
        title = yt.title.replace('|', '').replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('"', '').replace('*', '').replace('<', '').replace('>', '')
        print(f"[#] Downloading: {title}", end='\r')
        audio = yt.streams.filter(only_audio=True).first()
        temp_file = audio.download(output_path=os.path.join(download_dir,"MP3 Youtube Downloader"), filename="temp_audio")
        new_file = os.path.join(download_dir,"MP3 Youtube Downloader", title + '.mp3')
        if os.path.exists(os.path.join(download_dir,"MP3 Youtube Downloader", title + '.mp3')):
            i = 1
            while True:
                new_file = os.path.join(download_dir,"MP3 Youtube Downloader", f"{title} ({i}).mp3")
                if not os.path.exists(new_file):
                    title = f"{title} ({i})"
                    break
                i += 1
        os.rename(temp_file, new_file)
        print(f"[#] Success download: {title}\nThe downloaded file is located in the directory: {os.path.join(download_dir, "MP3 Youtube Downloader")}")
        with open(os.path.join(download_dir,"MP3 Youtube Downloader", "log.txt"), 'a') as log_file:
            x = dt.datetime.now()
            log_file.write(f"[{x.strftime("%y/%m/%d %H:%M")}] URL: {url}, title:{title}\n")
    except Exception as e:
        print(f"[#] Error: {str(e)}")


if __name__ == "__main__":
    if not os.path.exists(os.path.join(download_dir, "MP3 Youtube Downloader")):
        os.makedirs(os.path.join(download_dir, "MP3 Youtube Downloader"))
    if len(sys.argv) > 1:
        download_audio(sys.argv[1])
    else:
        print("mp3yt (1.1.2) by Fawwas Aliy\nusage: mp3yt [YOUTUBE_URL]")

