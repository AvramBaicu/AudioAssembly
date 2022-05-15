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
        return render_template('report.html', data="")