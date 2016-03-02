import os, uuid
from flask import Blueprint, render_template, redirect, url_for, flash, Markup, current_app, send_file, send_from_directory
from werkzeug.utils import secure_filename
from webapp import mail
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


def send_notification(resource, url_download):
    subject_owner = current_app.config['MAIL_NOTIFICATION_OWNER_SUBJECT']
    subject_receiver = current_app.config['MAIL_NOTIFICATION_RECEIVER_SUBJECT']
    body_owner = current_app.config['MAIL_NOTIFICATION_OWNER_BODY']
    body_receiver = current_app.config['MAIL_NOTIFICATION_RECEIVER_BODY']
    email_owner = resource.email_owner.split(";")
    email_recipients = resource.email_receiver.split(";")
    mail.send_mail(subject_receiver,
                   body_receiver.format(url_download=url_download),
                   email_recipients)
    mail.send_mail(subject_owner,
                   body_owner.format(url_download=url_download),
                   email_owner)


@listener.route("/", methods=['GET', 'POST'])
def resources():
    form = FormResource()
    if form.validate_on_submit():
        if form.attachment.has_file():
            remote_filename = secure_filename(form.attachment.data.filename)
            local_filename = str(uuid.uuid4())
            folder = os.path.join(os.getcwd(), current_app.config['UPLOAD_FOLDER'])
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_path = os.path.join(folder, local_filename)
            #TODO Encrypt file
            form.attachment.data.save(file_path)
            res = Resource.create(filename=remote_filename,
                            description=form.description.data,
                            path=file_path,
                            mimetype=form.attachment.data.mimetype,
                            email_owner=form.email_owner.data,
                            email_receiver=form.email_receiver.data)
            url_download = url_for('root.download', file_id=res.id)
            send_notification(res, url_download)
            flash(Markup('Resource added: <a href="{}">Download</a>'.format(url_download)))
            form = FormResource()
        else:
            flash(Markup('Can\'t do it without attachment'))
    return render_template('index.html',
                           form=form,
                           formats=htmlinput_accepted_formats())


@listener.route("/download/<int:file_id>", methods=['GET'])
def download(file_id):
    #TODO Decrypt file
    res = Resource.get(Resource.id == file_id)
    return send_file(filename_or_fp=res.path,
                     mimetype=res.mimetype,
                     as_attachment=True,
                     attachment_filename=res.filename)
