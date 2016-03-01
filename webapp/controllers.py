from flask import Blueprint, render_template, redirect, url_for
from webapp.forms import FormResource

__author__ = 'paxet'

listener = Blueprint('root', __name__)


@listener.route('/')
def index():
    return render_template('index.html', form=FormResource())


@listener.route("/new", methods=['POST'])
def new():
    form = FormResource()
    if form.validate_on_submit():
        if form.attachment.has_file():
            filename = secure_filename(form.attachment.data.filename)
            file_path = 'uploads/' + filename
            form.attachment.data.save(file_path)
            mimetype = form.attachment.data.mimetype
            Resource.create(filename=filename,
                            description=form.description.data,
                            path=file_path,
                            mimetype=mimetype)
            # TODO Send email to inform
            flash(Markup('Resource added'))
        else:
            flash(Markup('Can\'t do it without attachment'))
    return redirect(url_for('index'))
