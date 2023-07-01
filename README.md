# dm-tutorial-chat

- Download audio of youtube videos (either via scripts/get_audio_from_youtube_channel.py or scripts/get_audio_from_youtube_video_list.py)
- Transcribe audio via scripts/run_whisper.py
- Put them in a vector store with scripts/vecstore.py
- Set up Slack bot via __init__.py that allows 
    - for similarity search over documents in vector store 
    - and then passes them to openai to formulate an answer
    - which is passed back to Slack

./scripts/audio contains the downloaded audio tracks of the youtube videos
./scripts/audio_transcription contains the audio transcripts
./scripts/audio_transcription/episodes.csv contains metadata of the youtube videos
./scripts/faiss_index contains the vector store

./public contains the YouTube thumbnails of the videos