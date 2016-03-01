import os
from flask import Blueprint, render_template, redirect, url_for, flash, Markup, current_app
from werkzeug.utils import secure_filename
from webapp.forms import FormResource
from webapp.models import Resource

__author__ = 'paxet'

listener = Blueprint('root', __name__)


def htmlinput_accepted_formats():
    strfileformats = ''
    for fmt in current_app.config['FILE_FORMATS']:
        if len(strfileformats) >= 1:
            strfileformats += ', '
        strfileformats += '.' + fmt
    return strfileformats

@listener.route("/", methods=['GET', 'POST'])
def resources():
    form = FormResource()
    if form.validate_on_submit():
        if form.attachment.has_file():
            filename = secure_filename(form.attachment.data.filename)
            print(filename)
            folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_path = folder + '/' + filename
            print(file_path)
            form.attachment.data.save(file_path)
            mimetype = form.attachment.data.mimetype
            Resource.create(filename=filename,
                            description=form.description.data,
                            path=file_path,
                            mimetype=mimetype,
                            email_owner=form.email_owner.data,
                            email_receiver=form.email_receiver.data)
            # TODO Send email to inform
            flash(Markup('Resource added'))
            form = FormResource()
        else:
            flash(Markup('Can\'t do it without attachment'))
    return render_template('index.html',
                           form=form,
                           formats=htmlinput_accepted_formats())
