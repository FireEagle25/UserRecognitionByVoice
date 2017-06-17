from peewee import *

from UserIdentificationModule.Models.Configs.conf import db


class SqlLiteModel(Model):
    class Meta:
        database = db
