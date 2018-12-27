from pytube import YouTube
import os


class GetYoutubeFile:
    def __init__(self):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    def downloadYouTube(self, videourl, path):
        yt = YouTube(videourl)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not os.path.exists(path):
            os.makedirs(path)
        yt.download(path)

def main():
    gyt = GetYoutubeFile()  
    # selenium tutorial: O--WVte1WhU
    url = 'https://www.youtube.com/watch?v=O--WVte1WhU'
    savepath = os.path.abspath('../data/YouTube')
    print(savepath)
    gyt.downloadYouTube(url, savepath)

if __name__ == '__main__':
    main()
