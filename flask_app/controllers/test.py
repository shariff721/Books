from flask_app import app
from flask import render_template, redirect


@app.route('/')
def index():
    return "hello"