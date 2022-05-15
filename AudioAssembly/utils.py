import requests, os, re

disfluencies=re.compile("^(um+|uh+|hm+|mhm+|uh\shuh)$")

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

def interpret_data(data):
    confidence=str(data['confidence']*100)+"%"
    speakers=1
    disfluencies_count=0
    profanity=0
    for word in data["words"]:
        if word["speaker"] and ord(word["speaker"])-64 > speakers:
            speakers=ord(word["speaker"])-64
        if disfluencies.match(word["text"].replace(",", "").replace(".", "").replace(";", "").lower()):
            disfluencies_count+=1
        if "*" in word["text"]:
            profanity+=1
    language=data["language_code"]
    if "en" in language:
        language="English"
    elif language=="es":
        language="Spanish"
    elif language=="fr":
        language="French"
    elif language=="de":
        language="German"
    elif language=="it":
        language="Italian"
    keywords=[]
    if data["auto_highlights_result"]:
        keywords=data["auto_highlights_result"]["results"]
    tone={"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    if data["sentiment_analysis_results"]:
        for result in data["sentiment_analysis_results"]:
            tone[result["sentiment"]]+=1
        tone["POSITIVE"] = str((tone["POSITIVE"]/len(data["sentiment_analysis_results"]))*100)+"%"
        tone["NEGATIVE"] = str((tone["NEGATIVE"]/len(data["sentiment_analysis_results"]))*100)+"%"
        tone["NEUTRAL"] = str((tone["NEUTRAL"]/len(data["sentiment_analysis_results"]))*100)+"%"
    important_entities=data["entities"]
    content_safety=0
    content_safety_total=0
    if data["content_safety_labels"]:
            for result in data["content_safety_labels"]["results"]:
                for label in result["labels"]:
                    if label["severity"]:
                        content_safety+=label["severity"]
                        content_safety_total+=1
            if content_safety_total > 0:
                content_safety=str((content_safety/content_safety_total)*100)+"%"
    return {
        "confidence": confidence, # this returns a percentage
        "speakers": speakers, # this returns the number of speakers
        "disfluencies_count": disfluencies_count, # this returns the number of "ums"
        "language": language, # this returns the language
        "profanity": profanity, # this returns the number of swear words
        "keywords": keywords, # this returns an array of key words
        "content_safety": content_safety, # this returns a percentage
        "tone": tone, # this returns a string (e.g. POSITIVE)
        "important_entities": important_entities # this returns an array of important bodies
    }