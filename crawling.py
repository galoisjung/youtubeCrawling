import json

import requests
from urllib.parse import urlparse

import dao
import pytube_engine


def connection(query):
    URL_SEARCH = "https://www.googleapis.com/youtube/v3/search"
    resp = requests.get(URL_SEARCH, query)

    return resp.json()


def making_URL_list(js):
    y_url_list = list()
    for i in js['items']:
        y_url = i["id"]['videoId']
        y_url_list.append("https://www.youtube.com/watch?v=" + y_url)

    return y_url_list

