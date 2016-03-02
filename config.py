import os
from base64 import b64encode

__author__ = 'paxet'

APP_NAME = 'tyrachinas'

# SERVER_NAME = 'localhost'
SECRET_KEY = b64encode(os.urandom(64)).decode('utf-8')[:30]
WTF_CSRF_KEY = b64encode(os.urandom(64)).decode('utf-8')[:30]
WTF_CSRF_SECRET_KEY = b64encode(os.urandom(64)).decode('utf-8')[:30]

MAIL_SERVER = 'localhost'
MAIL_PORT = '25'
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = 'info@{}.io'.format(APP_NAME)
MAIL_NOTIFICATION_OWNER_SUBJECT = 'Sharing knowledge, new file added'
MAIL_NOTIFICATION_RECEIVER_SUBJECT = 'File shared by a collegue is awaiting'
MAIL_NOTIFICATION_OWNER_BODY = 'You\'ve updloaded a file. Download link is {url_download}'
MAIL_NOTIFICATION_RECEIVER_BODY = 'To get the file you must access {url_download}'

UPLOAD_FOLDER = 'uploads'
FILE_FORMATS = ['zip', '7z', 'tgz', 'gz', 'bz', 'rar']
