from flask import render_template, request
from AudioAssembly import app
from AudioAssembly.utils import upload_file, generate_transcript, get_transcript, interpret_data

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/report", methods=["POST"])
def report():
    upload_url = upload_file(request.files["data"])
    if upload_url:
        return render_template('report.html', data=interpret_data(get_transcript(generate_transcript(upload_url))))
    else:
        return render_template('report.html', data = {
        "confidence": "92%",
        "speakers": 1,
        "disfluencies_count": 1,
        "language": "English",
        "profanity": 1,
        "keywords": ["a", "b", "c"],
        "content_safety": "13%",
        "tone": {"POSITIVE": "20%", "NEGATIVE": "20%", "NEUTRAL": "20%"},
        "important_entities": [{"entity_type": "event", "text": "materialgirl"}, {"entity_type": "event", "text": "materialgirl"}]
    })