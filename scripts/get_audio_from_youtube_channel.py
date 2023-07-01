# retrieve audio files from youtube channel

import os
import requests
import yt_dlp
import pandas as pd
from youtubesearchpython import *

# Videos
channel_id = "UCEr-xMU78XORzBKII6NGGAQ"  # digital methods
playlist = Playlist(playlist_from_channel_id(channel_id))

# Episode data
stor_metadata = pd.DataFrame()
for v in playlist.videos:
    try:
        stor_metadata.loc[v['title'], 'id'] = v['id']
        stor_metadata.loc[v['title'], 'link'] = v['link']
        stor_metadata.loc[v['title'], 'title'] = v['title']
        stor_metadata.loc[v['title'], 'img'] = v['thumbnails'][3]['url']
    except:
        print("Failed on %s", v['title'])

# store audio of all videos
for ix in stor_metadata.index:

    img_url = stor_metadata.loc[ix, 'img']
    ep_link = stor_metadata.loc[ix, 'link']
    ep_id = stor_metadata.loc[ix, 'id']
    # if file does not exist
    if not os.path.exists("audio/%s.m4a" % str(ep_id)):
        # Write img
        with open("../public/%s.jpg" % str(ep_id), 'wb') as f:
            response = requests.get(img_url)
            f.write(response.content)
        # Write audio
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': 'audio/%s.m4a' % str(ep_id),
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(ep_link)

stor_metadata.reset_index().to_csv("audio_transcription/episodes.csv")
