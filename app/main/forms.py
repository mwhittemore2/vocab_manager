from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class SourceTextForm(FlaskForm):
    filename = FileField("File to analyze")
    submit = SubmitField("Submit")
