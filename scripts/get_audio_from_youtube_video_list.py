# retrieve audio files from youtube channel

import os
import requests
import yt_dlp
import pandas as pd
from youtubesearchpython import *

# Videos
# use pandas to read video_list.csv
video_list = pd.read_csv("video_list.csv")
# get video ids
video_ids = video_list['YouTube video id'].tolist()
# unique video ids
video_ids = list(set(video_ids))

# video data
stor_metadata = pd.DataFrame()

# loop over video ids
# store title, id, link, title, and img in a dataframe
for video_id in video_ids:
    v = Video.getInfo(video_id, mode=ResultMode.json)

    try:
        new_ep = pd.DataFrame(
            {'id': [video_id], 'link': [v['link']], 'title': [v['title']], 'img': [v['thumbnails'][2]['url']]})
        stor_metadata = pd.concat([stor_metadata, new_ep], ignore_index=True)
        print(video_id + "\t" + v['title'])
    except Exception as e:
        print(e)
        print("Failed on %s\t%s" % (video_id, v['title']))

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
