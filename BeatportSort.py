import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sys
from sys import argv
import shutil
import os
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def getURL(query):
    query = "Beatport " + query
    urls = []
    for url in search(query, tld="com", num=1, stop=3, pause=2):
        urls.append(url)
    return urls


def getGenre(url):
    if "https://www.beatport.com/track/" in url:
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        li = soup.findAll(
            'li', {"class": "interior-track-content-item interior-track-genre"})
        try:
            return li[0].a.string
        except IndexError:
            return "GENRE NOT FOUND"
    else:
        return "BEATPORT LINK NOT FOUND"


def getFilenames(path, filetype):
    fileDirectorys = []
    fileNames = []
    # taken from: https://mkyong.com/python/python-how-to-list-all-files-in-a-directory/
    # r=root, d=directories, f = files
    for r, _, f in os.walk(path):
        for file in f:
            if filetype in file:
                fileDirectorys.append(os.path.join(r, file))

    for f in fileDirectorys:
        filename = f.split('/')[-1].split(filetype)[0]
        fileNames.append(filename)

    return fileDirectorys, fileNames


def sortFiles(path, filetype):
    directorys, names = getFilenames(path, filetype)
    for name, directory in zip(names, directorys):
        urls = getURL(name)
        genres = []
        if not urls == []:
            for url in urls:
                urlGenre = getGenre(url)
                if not (urlGenre in ["GENRE NOT FOUND", "BEATPORT LINK NOT FOUND"]):
                    genres.append(urlGenre)
            if len(genres) > 0:
                print(genres)
                genre = genres[0]
            else:
                genre = "GENRE NOT FOUND"
        else:
            genre = "FailedURL"

        print("{:<17s}:\t{:<10s}".format(genre, name))
        oldPath = directory
        newDirectory = "/Users/MaxPilling/Music/Traktor Music/2020/Electronic/" + genre
        newPath = newDirectory + "/" + name + filetype
        if not os.path.exists(newDirectory):
            os.makedirs(newDirectory)

        shutil.move(oldPath, newPath)


if argv[1]:
    for filetype in [".mp3", ".flac", ".wav", ".m4a"]:
        sortFiles(argv[1], filetype)
else:
    print("please enter a directory")
