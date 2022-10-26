import os
import re
from googleapiclient.discovery import build
from pytube import YouTube
import hashlib
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
import dao
from oauth2client import file


def hashing(st):
    result = int.from_bytes(hashlib.sha256((st).encode()).digest()[:4], 'little')
    if int(result) < 1000000000:
        result = str(result) + "0"
    return result


def download(url, sqlcon_instance, already=[]):
    os.makedirs("youtube")
    alreadyh = []
    if len(already) != 0:
        for i in already:
            alreadyh.append(re.match("\d{10}", i).group())

    store = file.Storage('conf_DB.json')
    creds = store.get()

    Download_FOLDER = "./youtube"

    service = build('drive', 'v3', http=creds.authorize(Http()))
    if sqlcon_instance.drink:
        folder_id = "1It14LIYEcfttz3d5Y9hn33rKWPPwuwce"
    else:
        folder_id = "1ShlSdcGWQ1Snk6wJs3Ye42mBCwGsGA6X"

    yt = YouTube(url)
    h_name = hashing(yt.title)

    if str(h_name) not in alreadyh:
        print(yt.title)
        dao.add(yt, sqlcon_instance)
        stream = yt.streams.get_highest_resolution()

        stream.download(Download_FOLDER, filename_prefix=str(h_name))

        file_path = "./youtube/" + str(h_name) + yt.title

        request_body = {'name': file_path, 'parents': [folder_id],
                        'uploadType': 'multipart'}
        media = MediaFileUpload(file_path)
        file = service.files().create(body=request_body, media_body=media, fields='id').execute()

