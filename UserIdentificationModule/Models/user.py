from peewee import *

from UserIdentificationModule.Models.sqlLiteModel import SqlLiteModel


class User(SqlLiteModel):
    name = CharField()