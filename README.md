# DMI Tutorial Chat Bot

This chat bot was designed to serve the participants of the DMI summer school by addressing their queries related to topics found within previously recorded YouTube tutorials on digital methods. The process and results were genuinely captivating.

To create this bot, I started by assembling a comprehensive list of [75 DMI tutorials](https://github.com/ErikBorra/dm-tutorial-chat/blob/main/scripts/video_list.csv). I utilized [Whisper](https://openai.com/research/whisperhttps://openai.com/research/whisper) for transcribing each tutorial and stored these transcriptions in a vector database. The setup was such that users could make a query on the summer school's Slack. This query would then be matched with the database through a similarity search, yielding three snippets from the tutorial transcripts. The bot then incorporated these snippets along with the query to construct a response, using OpenAI's [GPT-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5https://platform.openai.com/docs/models/gpt-3-5). The answer, coupled with links to the videos from which the snippets were derived, was then forwarded to the user.

The bot performed exceptionally well in extracting information that could be found within a transcript window of approximately 5 minutes (as defined in my app). However, it struggled to handle overarching queries that were not explicitly addressed in the transcripts or questions not found in the tutorials. Even though the bot wouldn't produce answers to questions it has no knowledge of, it tended to overextend - or 'hallucinate' - when presented with questions that seemed vaguely related to some content.


# Instructions of use

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

