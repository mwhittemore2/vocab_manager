from flask import render_template, redirect, url_for
from . import main
from .forms import SourceTextForm

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/upload_source", methods=['GET', 'POST'])
def upload_source():
    source_text = None
    form = SourceTextForm()
    if form.validate_on_submit():
        data = form.filename.data
        for line in data:
            print(line)
        return redirect(url_for('.upload_source'))
    return render_template("upload_source.html", form=form)
