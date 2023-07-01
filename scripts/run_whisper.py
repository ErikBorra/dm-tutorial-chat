# transcribe audio
# (Instead we may just want to use the YouTubeTranscriptAPI, see e.g. https://github.com/the-full-stack/ask-fsdl/blob/charles/etl-modal/Building%20the%20Document%20Corpus.ipynb)
import time
import os
import logging
import whisper  # pip3.10 install git+https://github.com/openai/whisper.git
import numpy as np
import pandas as pd

# Set up logger
logging.basicConfig(filename='whisper.log', filemode='w', level=logging.DEBUG)

# Read the csv file
new_ep = pd.read_csv("audio_transcription/episodes.csv", index_col=None)

# Run whisper on each audio file
for ix in new_ep.index:

    ep_id = new_ep.loc[ix, 'id']
    print("Processing %s" % ep_id)

    audio_file_path = 'audio/%s.m4a' % str(ep_id)
    out_file_path = 'audio_transcription/%s.txt' % str(ep_id)

    # if file does not exist
    if os.path.exists(out_file_path):
        print(out_file_path + " already exists")
        continue

    print(f"Processing file: {audio_file_path}")
    start_time = time.time()

    # load Whisper model and transcribe audio file
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_path)

    # write
    with open(out_file_path, "w") as f:
        for seg in result['segments']:
            ts = np.round(seg['start'], 1)
            f.write(new_ep.loc[ix, 'link'] + "&t=%ss" %
                    ts + "\t" + str(ts) + "\t" + seg['text'] + "\n")

    end_time = time.time()
    time_diff = end_time - start_time
    print(f"Time taken: {time_diff:.2f} seconds")
