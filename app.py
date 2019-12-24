from flask import Flask, request, redirect, url_for, render_template
from pytube import YouTube, Playlist
import pytube.exceptions
import os
import re
import urllib.request
import requests

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
        wtw = ['https://www.youtube.com/watch', 'https://m.youtube.com/watch']
        wtm = 'https://youtu.be'
        pl = 'https://www.youtube.com/playlist'
        if wtw[0] in url_dw or wtw[1] in url_dw:
            try:
                yt = get_watch_stream(url_dw)
            except KeyError:
                return render_template('index.html', eval=1)
            except pytube.exceptions.RegexMatchError:
                return render_template('index.html', eval=1)
            return render_template('result.html', yt=yt, wtpt='wt')
        elif wtm in url_dw:
            murl = 'https://www.youtube.com/watch?v=' + url_dw.split('.be/')[1]
            try:
                yt = get_watch_stream(murl)
            except KeyError:
                return render_template('index.html', eval=1)
            except pytube.exceptions.RegexMatchError:
                return render_template('index.html', eval=1)
            return render_template('result.html', yt=yt, wtpt='wt')
        elif pl in url_dw:
            try:
                pt = get_playlist_urls(url_dw).parse_links()
                for link in pt:
                    urlList.append('https://www.youtube.com/' + link)
                for y in urlList:
                    streamListDict[y] = get_watch_stream(y)
                streamListDictList = [(k, v) for k, v in streamListDict.items()]
            except KeyError:
                return render_template('index.html', eval=1)
            except pytube.exceptions.RegexMatchError:
                return render_template('index.html', eval=1)
            except pytube.exceptions.VideoUnavailable:
                return render_template('index.html', eval=1)
            return render_template('result.html', streamListDictList=streamListDictList, wtpt='pt')
        else:
            return render_template('index.html', eval=1)
    else:
        return render_template('index.html', eval=1)


@app.route('/download', methods=['GET', 'POST'])
def download_page():
    wtpt = ''
    if request.method == 'POST':
        wtw = ['https://www.youtube.com/watch', 'https://youtube.com/watch', ]
        wtm = 'https://youtu.be/'
        pt = 'https://www.youtube.com/playlist'
        if wtw[0] in gurl_dw or wtw[1] in gurl_dw:
            download_itag = request.form['download']
            try:
                get_watch_stream(gurl_dw).streams.get_by_itag(download_itag).download(filename="youtubeVideo")
            except KeyError:
                return render_template('index.html', eval=1)
            except pytube.exceptions.RegexMatchError:
                return render_template('index.html', eval=1)
            return render_template('download.html', wtpt='wt')
        elif wtm in gurl_dw:
            download_itag = request.form['download']
            murl = 'https://www.youtube.com/watch?v=' + gurl_dw.split('.be/')[1]
            try:
                get_watch_stream(murl).streams.get_by_itag(download_itag).download(filename="youtubeVideo")
            except KeyError:
                return render_template('index.html', eval=1)
            except pytube.exceptions.RegexMatchError:
                return render_template('index.html', eval=1)
            return render_template('download.html', wtpt='wt')
        elif pt in gurl_dw:
            if request.form["download"] == "Download":
                download_itag_url_wt = request.form['downloadItag']
                download_itag_url_wt_list = download_itag_url_wt.split(", ")
                download_itag = download_itag_url_wt_list[1]
                download_url = download_itag_url_wt_list[0]
                try:
                    get_watch_stream(download_url).streams.get_by_itag(download_itag).download()
                except KeyError:
                    return render_template('index.html', eval=1)
                except pytube.exceptions.RegexMatchError:
                    return render_template('index.html', eval=1)
                return render_template('download.html', wtpt='pt')
            elif request.form["download"] == "Download All":
                try:
                    get_playlist_urls(gurl_dw).download_all()
                except KeyError:
                    return render_template('index.html', eval=1)
                except pytube.exceptions.RegexMatchError:
                    return render_template('index.html', eval=1)
                return render_template('download.html', wtpt='pt')
        else:
            return render_template('index.html', eval=1)
    else:
        return render_template('index.html', eval=1)


@app.route('/facebook_download', methods=['POST', 'GET'])
def facebook_download():
    url_fb = 'https://www.facebook.com/'
    if request.method == 'POST':
        url = request.form['fburl']
        resolution = request.form['sdhd']
        if url_fb in url:
            url_fb_videos = url_fb + url.split('/videos')[0].split('.com/')[1] + '/videos/'
            if url_fb_videos in url:
                try:
                    download_Video(url,resolution)
                except TypeError:
                    return render_template('index.html', evalfb=1)
            else:
                return render_template('index.html', evalfb=1)
        else:
            return render_template('index.html', evalfb=1)
        return render_template('download.html',wtpt='fb')
    else:
        return render_template('index.html', evalfb=1)


def get_watch_stream(url):
    yt = YouTube(url)
    return yt


def get_playlist_urls(playlist_url):
    pt = Playlist(playlist_url)
    return pt


def extract_url(html, quality):
    if quality == "sd":
        url = re.search('sd_src:"(.+?)"', html)[0]
    else:
        url = re.search('hd_src:"(.+?)"', html)[0]
    url = url.replace('hd_src:"', '')
    url = url.replace('sd_src:"', '')
    url = url.replace('"', "")
    print(url)
    return url


def download_Video(url, resolution):
    r = requests.get(url)
    file_url = extract_url(r.text, resolution)
    path = "FacebookVideo" + ".mp4"
    #urllib.request.urlretrieve(file_url, path)


def delete_downloaded_video():
    os.remove("youtube.mp4")


def delete_downloaded_folder():
    # TODO:deletefolder
    pass


if __name__ == '__main__':
    app.run(debug=True)
