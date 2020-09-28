from flask import render_template
from . import main

@main.route("/")
def index():
    """
    Renders the entry point to the application.
    """
    return render_template("index.html")