import requests
from bs4 import BeautifulSoup
from pathlib import Path
from sys import argv
import shutil
import os
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def getURL(query):
    query = "Beatport " + query

    for j in search(query, tld="com", num=1, stop=1, pause=2):
        url = j
    return url


def getGenre(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    li = soup.findAll(
        'li', {"class": "interior-track-content-item interior-track-genre"})
    try:
        return li[0].a.string
    except IndexError:
        return 'GENRE NOT FOUND'


def getFilenames(path):
    fileDirectorys = []
    fileNames = []
    # taken from: https://mkyong.com/python/python-how-to-list-all-files-in-a-directory/
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.mp3' in file:
                fileDirectorys.append(os.path.join(r, file))

    for f in fileDirectorys:
        filename = f.split('/')[-1].split('.mp3')[0]
        fileNames.append(filename)

    return fileDirectorys, fileNames


def sortFiles():
    directorys, names = getFilenames(argv[1])
    for name, directory in zip(names, directorys):
        genre = getGenre(getURL(name))
        print("{0}:     {1}".format(name, genre))
        oldPath = directory
        newDirectory = "/Users/MaxPilling/Music/Traktor Music/2020/Electronic/" + genre
        newPath = newDirectory + "/" + name + ".mp3"

        if not os.path.exists(newDirectory):
            os.makedirs(newDirectory)

        shutil.move(oldPath, newPath)


sortFiles()
