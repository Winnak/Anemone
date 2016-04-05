""" Data models for the database """
# pylint: disable=R0903
# pylint: disable=C0103

import peewee
from flask.json import JSONEncoder
import Anemone.database

class BaseModel(peewee.Model):
    """ Base model for all the models """
    class Meta:
        """ meta data """
        database = Anemone.database.DATABASE

class Project(BaseModel):
    """ Data model for Projects table """
    name = peewee.CharField()
    slug = peewee.CharField(unique=True)
    filepath = peewee.CharField(null=True)
    description = peewee.TextField(null=True)

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

class ProjectJSONEncoder(JSONEncoder):
    """ Custom json encoder for the projects class """
    #pylint: disable=E0202
    def default(self, obj): #override
        if isinstance(obj, Project):
            return dict(name=obj.name, slug=obj.slug, filepath=obj.filepath,
                        description=obj.description)
        else:
            JSONEncoder.default(self, obj)
    #pylint: enable=E0202
