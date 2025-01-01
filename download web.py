import requests
import yt_dlp
from flask import Flask,render_template,request

def download_file(url,a):
    with requests.get(url,stream=True) as r:
        r.raise_for_status()
        with open(a,'wb') as f:
            for i in r.iter_content(chunk_size=8192):
                f.write(i)
    return a

def download_audio(url,a):
    ydl_opts={
        'format':'bestaudio/best',
        'outtmpl':a,
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'
        }],
    }
    yt_dlp.YoutubeDL(ydl_opts).download([url])
    return a

def download_media(url, a, cookies_path=r"C:\Users\krish\OneDrive\Desktop\code\instagram\cookies.txt"):
    ydl_opts = {
        'outtmpl': a,
        'format': 'bestvideo[height<=720]+bestaudio/best',
        'merge_output_format': 'mp4',
        'postprocessors': [{'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
        }],
        'verbose': True
    }
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path
    
    yt_dlp.YoutubeDL(ydl_opts).download([url])
    return a


def download(url,a):
    if a.lower().endswith('.mp3'):
        return download_audio(url,a)
    elif a.lower().endswith('.mp4'):
        return download_media(url,a)
    else:
        return download_file(url,a)

app=Flask(__name__)

@app.route('/')
def form():
    return render_template("index.html")

@app.route("/submit",methods=['POST'])
def submit():
    url=request.form['url']
    file=request.form['file']
    exe=request.form['exe']
    file1=f"{file}.{exe}"
    download(url,file1)
    return "download complete"

if __name__ == '__main__':
    app.run(debug=True)