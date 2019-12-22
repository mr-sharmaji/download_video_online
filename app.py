from flask import Flask, request, redirect, url_for, render_template
from pytube import YouTube, Playlist
import os

app = Flask(__name__)

gurl_dw = ''


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def result_page():
    global gurl_dw
    wtpt = ''
    urlList = list()
    streamListDict = dict()
    streamListDictList = list()
    if request.method == 'POST':
        url_dw = request.form['url']
        gurl_dw = url_dw
        wt = 'https://www.youtube.com/watch'
        pl = 'https://www.youtube.com/playlist'
        if wt in url_dw:
            yt = get_watch_stream(url_dw)
            print(type(yt.streams.first().itag))
            return render_template('result.html', yt=yt, wtpt='wt')
        elif pl in url_dw:
            pt = get_playlist_urls(url_dw).parse_links()
            for link in pt:
                urlList.append('https://www.youtube.com/' + link)
            for y in urlList:
                streamListDict[y] = get_watch_stream(y)
            streamListDictList = [(k, v) for k, v in streamListDict.items()]
            return render_template('result.html', streamListDictList=streamListDictList, wtpt='pt')
        else:
            return render_template('index.html', eval=1)
    else:
        return render_template('index.html', eval=1)


@app.route('/download', methods=['GET', 'POST'])
def download_page():
    wtpt = ''
    if request.method == 'POST':
        wt = 'https://www.youtube.com/watch'
        pt = 'https://www.youtube.com/playlist'
        if wt in gurl_dw:
            download_itag = request.form['download']
            download_stream = get_watch_stream(gurl_dw).streams.get_by_itag(download_itag)
            return render_template('download.html', wtpt='wt')
        elif pt in gurl_dw:
            print(request.form['download'])
            if request.form["download"] == "Download":
                download_itag_wt = request.form['downloadItag']
                get_watch_stream(gurl_dw).streams.get_by_itag(download_itag_wt).download()
                return render_template('download.html', wtpt='pt')
            elif request.form["download"] == "Download All":
                get_playlist_urls(gurl_dw).download_all()
                return render_template('download.html', wtpt='pt')
    else:
        return render_template('index.html', eval=1)


def get_watch_stream(url):
    yt = YouTube(url)
    return yt


def get_playlist_urls(playlist_url):
    pt = Playlist(playlist_url)
    return pt


def delete_downloaded_video():
    os.remove("youtube.mp4")


def delete_downloaded_folder():
    # TODO:deletefolder
    pass


if __name__ == '__main__':
    app.run(debug=True)
