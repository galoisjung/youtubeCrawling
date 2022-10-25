import json
import os

import crawling
import pytube_engine
import dao


def let_download(page, sql_connection=dao.connection_sqlite):
    if os.path.isdir("youtube"):
        already_down = os.listdir("youtube")
    else:
        already_down = []

    with open("conf.json") as f:
        qr = json.load(f)

    sqlcon_instance = sql_connection(True)

    for i in range(page + 1):
        js = crawling.connection(qr)
        if js['nextPageToken'] != None:
            qr["pageToken"] = js['nextPageToken']
        else:
            break
        result = crawling.making_URL_list(js)

        if i != 0:
            for j in result:
                pytube_engine.download(j, sqlcon_instance, already_down)
