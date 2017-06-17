from peewee import *

from UserIdentificationModule.Models.sqlLiteModel import SqlLiteModel
from UserIdentificationModule.Models.user import User


class Record(SqlLiteModel):
    filename = CharField()
    owner = ForeignKeyField(User, related_name='records')
