import os
import locale
from flask import Flask, g, request, url_for, render_template
from werkzeug.contrib.fixers import ProxyFix
from webapp import db
from webapp.mail import mailer
from webapp.controllers import listener

__author__ = 'paxet'
__version__ = '0.1.0.dev1'
__description__ = 'Simple web app to host and share files'

if os.name == 'nt':
    locale.setlocale(locale.LC_ALL, 'Spanish')  # Windows
else:
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')  # other (unix)

app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    # Production runs behind a proxy
    app.wsgi_app = ProxyFix(app.wsgi_app)

# Initialize Database
database = db.get_db()

# Setup Flask-Mail
mailer.init_app(app)

# Loading blueprints
app.register_blueprint(listener)


# Jinja Templates Filters
@app.template_filter()
def floathumanreadable(number: float):
    return locale.format("%.2f", number, True, True)


@app.errorhandler(401)
def forbidden_401(exception):
    return render_template('errors/401.html', exception=exception), 401


@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('errors/403.html', exception=exception), 403


@app.errorhandler(404)
def forbidden_404(exception):
    return render_template('errors/404.html', exception=exception), 404


# Open connection on request
@app.before_request
def before_request():
    g.db = database
    g.db.connect()


# Closing connection after request
@app.teardown_request
def teardown_request(exc):
    if not g.db.is_closed():
        g.db.close()
