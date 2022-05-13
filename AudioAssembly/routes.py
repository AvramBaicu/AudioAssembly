from flask import render_template, request, url_for, redirect
from AudioAssembly import app, db
from AudioAssembly.models import element

@app.route("/")
def index():
    return render_template('index.html', db=[])

@app.route("/add", methods=["POST"])
def add():
    return redirect(url_for('index'))

@app.route("/update/<id>", methods=["POST"])
def update(id):
    return redirect(url_for('index'))

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    return redirect(url_for('index'))