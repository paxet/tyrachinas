import datetime
from peewee import CharField, TextField, BooleanField, DateTimeField, IntegerField, ForeignKeyField
from webapp.db import BaseModel

__author__ = 'paxet'


class Resource(BaseModel):
    filename = CharField(max_length=255)
    description = TextField()
    email_owner = CharField(max_length=255)
    email_receiver = CharField(max_length=255)
    path = CharField(null=True)
    uploaded_date = DateTimeField(default=datetime.datetime.now)
    mimetype = CharField(null=True, max_length=255)
    encrypted = BooleanField(default=False)

    class Meta:
        order_by = ('uploaded_date',)

    def __str__(self):
        return '{}: {}'.format(self.uploaded_date, self.filename)
