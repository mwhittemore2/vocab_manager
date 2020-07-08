from flask import current_app
from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app import languages

class SourceTextForm(FlaskForm):
    """
    Assists a user in uploading a document.
    """
    #Document Title
    title_validators = [DataRequired(), Length(1,256)]
    title = StringField('Title', validators=title_validators)

    #Document Author
    author_validators = [DataRequired(), Length(1,256)]
    author = StringField('Author', validators=author_validators)

    #Document Language
    lang_options = languages
    language = SelectField('Language', choices=lang_options)

    #Document Text
    filename = FileField('Document to upload')

    #Submit Form
    submit = SubmitField("Submit")