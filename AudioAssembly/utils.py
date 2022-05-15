from flask import request, render_template
import requests, os

# helper function retrieved from AssemblyAI API
def read_file(file, chunk_size=5242880):
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data

def upload_file(audio):
    if not audio.filename:
        return None
    headers={'authorization': os.environ.get("AAI_API_KEY")}
    response=requests.post('https://api.assemblyai.com/v2/upload',
                        headers=headers,
                        data=read_file(audio))
    return response.json()['upload_url']

def generate_transcript(upload_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json={
        "audio_url": upload_url,
        "speaker_labels": True, # number of speakers
        "disfluencies": True, # filler words (count them manually)
        "language_detection": True, # detect the language of the speaker(s)
        "filter_profanity": True, # will be used to count profanity
        "auto_highlights": True, # key words
        "content_safety": True, # percentage of how safe content is (refer to docs for interpretation)
        "sentiment_analysis": True, # tone of speaker(s)
        "entity_detection": True # important entities mentioned
    }
    headers={
        "authorization": os.environ.get("AAI_API_KEY"),
        "content-type": "application/json"
    }
    response=requests.post(endpoint, json=json, headers=headers)
    return response.json()['id']

def get_transcript(id):
    endpoint="https://api.assemblyai.com/v2/transcript/" + id
    headers={
        "authorization": os.environ.get("AAI_API_KEY"),
    }
    response=requests.get(endpoint, headers=headers)
    while response.json()["status"] != "completed":
        response = requests.get(endpoint, headers=headers)
    return response.json()