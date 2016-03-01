import os
from base64 import b64encode

__author__ = 'paxet'

APP_NAME = 'tyrachinas'

SECRET_KEY = b64encode(os.urandom(64)).decode('utf-8')[:30]
WTF_CSRF_KEY = b64encode(os.urandom(64)).decode('utf-8')[:30]
WTF_CSRF_SECRET_KEY = b64encode(os.urandom(64)).decode('utf-8')[:30]

MAIL_SERVER = '172.26.26.32'
MAIL_PORT = '25'
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = 'marketing@ainia.es'
MAIL_DESTINATARIO_PRUEBAS = 'fjllopis@ainia.es'

UPLOAD_FOLDER = 'uploads'
FILE_FORMATS = ['zip', '7z', 'tgz', 'gz', 'bz', 'rar']
