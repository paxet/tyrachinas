import os
import uuid
from io import BytesIO
import random
import string
from flask import Blueprint, render_template, url_for, flash, \
    Markup, current_app, send_file, request, abort
from werkzeug.utils import secure_filename
from webapp import mail
from webapp.forms import FormResource
from webapp.models import Resource
from webapp.cipher import encrypt_stream, decrypt_stream, sha256key

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
    return True


def generate_password(length=32):
    myrg = random.SystemRandom()
    alphabet = string.ascii_letters + string.digits  # + string.punctuation
    return ''.join(myrg.choice(alphabet) for _ in range(length))


@listener.route("/", methods=['GET', 'POST'])
def resources():
    form = FormResource()
    if form.validate_on_submit():
        if form.attachment.has_file():
            remote_filename = secure_filename(form.attachment.data.filename)
            local_filename = str(uuid.uuid4())
            folder = os.path.join(os.getcwd(),
                                  current_app.config['UPLOAD_FOLDER'])
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_path = os.path.join(folder, local_filename)
            in_fh = BytesIO()
            form.attachment.data.save(in_fh)
            # Encrypt file
            password = generate_password()
            key = sha256key(password)
            with open(file_path, 'wb') as out_fh:
                encrypt_stream(key, in_fh, out_fh)
            # Save to database
            res = Resource.create(filename=remote_filename,
                                  description=form.description.data,
                                  path=file_path,
                                  mimetype=form.attachment.data.mimetype,
                                  email_owner=form.email_owner.data,
                                  email_receiver=form.email_receiver.data,
                                  encrypted=True)
            # Notify user
            url_download = url_for('root.download',
                                   file_id=res.id,
                                   password=password,
                                   _external=True)
            send_notification(res, url_download)
            msg = 'Resource added: <a href="{}">Download</a>'
            flash(Markup(msg.format(url_download)))
            form = FormResource()
        else:
            flash(Markup('Can\'t do it without attachment'))
    return render_template('index.html',
                           form=form,
                           formats=htmlinput_accepted_formats(),
                           appname=current_app.config['APP_NAME'])


@listener.route("/download/<int:file_id>", methods=['GET'])
def download(file_id):
    password = request.args.get('password', '')
    key = sha256key(password)
    print('La key: {}'.format(key))
    try:
        res = Resource.get(Resource.id == file_id)
    except Resource.DoesNotExist:
        abort(404)
    else:
        if res.encrypted:
            to_send = BytesIO()
            with open(res.path, 'rb') as in_fh:
                # to_send.write(decrypt_stream(fh, key))
                decrypt_stream(key, in_fh, to_send)
            to_send.seek(0)
        else:
            to_send = res.path
        return send_file(filename_or_fp=to_send,
                         mimetype=res.mimetype,
                         as_attachment=True,
                         attachment_filename=res.filename)
