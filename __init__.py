# interfaces between slack, vector store and open ai
# based on https://levelup.gitconnected.com/quickly-build-a-chatgpt-slack-bot-with-custom-data-using-python-and-openai-embeddings-b6d78c77980e

# run as python -u __init__.py 2>&1 | tee log.txt &
# then tail -f log.txt

import os
import re
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_executor import Executor
from slack_sdk import WebClient

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import FAISS  # pip install faiss-gpu

app = Flask(__name__)

# Credentials
load_dotenv("./scripts/.env")

# allows us to execute a function after returning a response
executor = Executor(app)

# set all our keys - use your .env file
slack_token = os.getenv('SLACK_TOKEN')
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
print(slack_token, VERIFICATION_TOKEN)

# instantiating slack client
slack_client = WebClient(slack_token)

# create a route for slack to hit


@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.data.decode("utf-8"))
    # look over the data being sent from slack
    # print(data)
    # check the token for all incoming requests
    if data["token"] != VERIFICATION_TOKEN:
        return {"status": 403}
    # confirm the challenge to slack to verify the url
    if "type" in data:
        if data["type"] == "url_verification":
            response = {"challenge": data["challenge"]}
            return jsonify(response)
    # handle incoming mentions
    if "@U05FTEKF0V6" in data["event"]["text"]:
        # executor will let us send back a 200 right away
        executor.submit(handleMentions, data["event"]["channel"], data["event"]["text"].replace(
            '<@U05FTEKF0V6>', '').strip(), data['event']['user'].strip())
        return {"status": 200}
    return {"status": 503}


def extract_urls(data):
    # Regular expression to find URLs
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # Find URLs in the "sources" field
    sources_urls = url_pattern.findall(data["sources"])

    # Find URLs in the "source_documents" field
    source_documents_urls = []
    for document in data["source_documents"]:
        # The following line assumes that the 'source' and 'link' fields are the only fields with URLs
        document_urls = url_pattern.findall(str(document))
        source_documents_urls += document_urls

    # Combine all URLs
    all_urls = sources_urls + source_documents_urls

    # remove duplicates
    unique_urls = list(
        set([url.replace("',", "").replace(",", "") for url in all_urls]))

    return unique_urls

# function to send back a message to slack


def handleMentions(channel, question, user):
    print("Q: " + question)
    if not os.path.exists("./scripts/faiss_index"):
        text = "I could not find a vector database. Please contact the administrator."
        # post message back to slack with the response
        slack_client.chat_postMessage(channel=channel, text=text)
    else:
        try:
            # create embeddings
            embeddings = OpenAIEmbeddings()
            # print("created embeddings")
            # load the vectorstore
            db = FAISS.load_local(
                "./scripts/faiss_index", embeddings)
            # print("loaded vectorstore")
            # expose this index in a retriever interface
            retriever = db.as_retriever(
                search_type="similarity", search_kwargs={"k": 3})
            # print("created retriever")
            # Build a QA chain
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            # print
            qa = RetrievalQAWithSourcesChain.from_chain_type(
                llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
            # print("created qa chain")

            a = qa({"question": question, "verbose": True},
                   return_only_outputs=False)

            answer = "<@" + user + "> "
            answer += re.sub(r'\(.*?\)', '', a["answer"])
            answer = answer.replace("\nSOURCES:", "")
            if not "There is no specific information provided" in answer:
                answer += "\nSources:"

                urls = extract_urls(a)
                for url in urls:
                    answer += "\n" + url

            print("A: " + answer + "\n")

            # post message back to slack with the response
            slack_client.chat_postMessage(channel=channel, text=answer)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Optionally send a message to the Slack channel about the error.
            slack_client.chat_postMessage(
                channel=channel, text=f"An error occurred: {str(e)}")


# run our app on port 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
