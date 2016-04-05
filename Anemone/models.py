""" Data models for the database """
# pylint: disable=R0903
# pylint: disable=C0103

import peewee
import Anemone.database

class BaseModel(peewee.Model):
    """ Base model for all the models """
    class Meta:
        """ meta data """
        database = Anemone.database.DATABASE

class Project(BaseModel):
    """ Data model for Projects table """
    name = peewee.CharField()
    slug = peewee.CharField()
    description = peewee.TextField()
    platforms = peewee.IntegerField()

class Job(BaseModel):
    """ Data model for Jobs table """
    id = peewee.PrimaryKeyField()
    project = peewee.ForeignKeyField(Project)
    status = peewee.IntegerField()
    name = peewee.CharField()
    description = peewee.TextField(null=True)
    log = peewee.TextField(null=True)
    started = peewee.DateTimeField(null=True)
    ended = peewee.DateTimeField(null=True)
