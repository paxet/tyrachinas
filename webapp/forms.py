from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.html5 import EmailField
from wtforms.fields import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
from config import FILE_FORMATS

__author__ = 'paxet'

class FormResource(Form):
    description = TextAreaField('Description', validators=[DataRequired(message='Introduce a short description')])
    attachment = FileField('Attachment', validators=[
        FileRequired(message='You\'ve forgot the attachment'),
        FileAllowed(FILE_FORMATS, 'Compressed files only!')
    ])
    email_owner = EmailField('Your address', validators=[DataRequired(message='Tell us who are you')])
    email_receiver = EmailField('Whom to notify', validators=[DataRequired(message='Someone to send the file')])
