from flask import current_app, flash, g, render_template

from . import content_management
from .forms import SourceTextForm
from .lib.resources import create_book
from .lib.upload import DocumentUploader

@content_management.route("/document_upload", methods=["GET", "POST"])
def document_upload():
    """
    Uploads a user-specified document to the database.
    """
    form = SourceTextForm()
    if form.validate_on_submit():
        doc = {}
        doc["file"] = form.filename.data
        doc["author"] = form.author.data
        doc["title"] = form.title.data
        doc["language"] = form.language.data

        params = {}
        params["email"] = g.current_user.email
        params["new_page"] = current_app.config["DOCUMENT_UPLOAD"]["PAGE_LIMIT"]
        params["line_size"] = current_app.config["DOCUMENT_UPLOAD"]["LINE_SIZE"]
        params["batch_size"] = current_app.config["DOCUMENT_UPLOAD"]["BATCH_SIZE"]
        params["tokenizer"] = current_app.config["TOKENIZER"].select(doc["language"])
        params["resource"] = create_book
        doc_uploader = DocumentUploader(params)
        
        could_upload = True
        try:
            doc_uploader.upload(doc)
        except Exception as e:
            could_upload = False
            error_msg = "Error uploading document. Please try again."
            flash(error_msg)

        if could_upload:
            success_msg = "Document successfully uploaded."
            flash(success_msg)

    return render_template('content_management/document_upload.html', form=form)