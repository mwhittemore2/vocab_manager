import traceback

from flask import current_app, flash, g, render_template
from flask_login import current_user, login_required

from . import cm
from .forms import SourceTextForm
from .lib.resources import create_book
from .lib.upload import DocumentUploader

@cm.route("/document_upload", methods=["GET", "POST"])
@login_required
def document_upload():
    """
    Uploads a user-specified document to the database.
    """
    form = SourceTextForm()
    if form.validate_on_submit():
        user = current_user

        doc = {}
        doc["file"] = form.filename.data
        doc["author"] = form.author.data
        doc["title"] = form.title.data
        doc["language"] = form.language.data

        params = {}
        params["email"] = user.email
        params["new_page"] = current_app.config["DOCUMENT_UPLOAD"]["PAGE_LIMIT"]
        params["line_size"] = current_app.config["DOCUMENT_UPLOAD"]["LINE_SIZE"]
        params["early_cutoff"] = current_app.config["DOCUMENT_UPLOAD"]["EARLY_CUTOFF"]
        params["batch_size"] = current_app.config["DOCUMENT_UPLOAD"]["BATCH_SIZE"]
        params["tokenizer"] = current_app.config["TOKENIZER"].select(doc["language"])
        params["resource"] = create_book
        doc_uploader = DocumentUploader(params)
        
        could_upload = True
        try:
            doc_uploader.upload(doc)
        except Exception as e:
            traceback.print_exc()
            could_upload = False
            error_msg = "Error uploading document. Please try again."
            flash(error_msg)

        if could_upload:
            success_msg = "Document successfully uploaded."
            flash(success_msg)

    return render_template('content_management/document_upload.html', form=form)

@cm.route("/select_content")
@login_required
def select_content():
    """
    Enables a user to choose one of the features that
    Vocabulary Manager offers.
    """
    return render_template('content_management/select_content.html')