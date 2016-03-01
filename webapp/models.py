import datetime
from peewee import CharField, TextField, BooleanField, DateTimeField, IntegerField, ForeignKeyField
from webapp.db import BaseModel

__author__ = 'paxet'


class Resource(BaseModel):
    filename = CharField(null=False, max_length=255)
    description = TextField(null=False)
    email_owner = CharField(null=False, max_length=255)
    email_receiver = CharField(null=False, max_length=255)
    path = CharField(null=True)
    uploaded_date = DateTimeField(datetime.datetime.now)
    mimetype = CharField(null=True, max_length=255)
    encrypted = BooleanField(default=False)

    class Meta:
        order_by = ('uploaded_date',)

    def __str__(self):
        return '{}: {}'.format(self.uploaded_date, self.filename)
