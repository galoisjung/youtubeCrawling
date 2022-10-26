import os
import re

from pytube import YouTube
import hashlib

import dao


def hashing(st):
    result = int.from_bytes(hashlib.sha256((st).encode()).digest()[:4], 'little')
    if int(result) < 1000000000:
        result = str(result) + "0"
    return result


def download(url, sqlcon_instance, already=[]):
    os.makedirs("youtube", exist_ok=True)
    alreadyh = []
    if len(already) != 0:
        for i in already:
            alreadyh.append(re.match("\d{10}", i).group())

    Download_FOLDER = "./youtube"
    yt = YouTube(url)
    h_name = hashing(yt.title)

    if str(h_name) not in alreadyh:
        print(yt.title)
        dao.add(yt, sqlcon_instance)
        stream = yt.streams.get_highest_resolution()
        stream.download(Download_FOLDER, filename_prefix=str(h_name))
