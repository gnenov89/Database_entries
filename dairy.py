import datetime
from peewee import *
import os
from collections import OrderedDict
import sys
#Creting database
db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db