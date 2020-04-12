import requests
from bs4 import BeautifulSoup
from pathlib import Path
from sys import argv
import os
from googlesearch import search


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
    print(li[0].a.string)


def getFilenames(directory):


getFilenames(argv[1])
# url = getURL(
#     "Dele Sosimi Afrobeat Orchestra - Too Much Information (Laolu Remix) (Edit)")
# getGenre(url)
