""" Data models for the database """

# pylint: disable=R0903
# disabling R0903: Too few public methods warning, because this file is meant to contain data models
# pylint: disable=C0103
# disabling C0103: Invalid class attribute name "id", this is a database convention.

import peewee
from flask.json import JSONEncoder
from Anemone import app

DATABASE = peewee.SqliteDatabase(app.config["DATABASE_PATH"])

class BaseModel(peewee.Model):
    """ Base model for all the models """
    class Meta:
        """ meta data """
        database = DATABASE

class Project(BaseModel):
    """ Data model for Projects table """
    name = peewee.CharField()
    slug = peewee.CharField(unique=True)
    filepath = peewee.CharField(null=True)
    description = peewee.TextField(null=True)
    output = peewee.CharField()
    created_at = peewee.DateTimeField()

class Job(BaseModel):
    """ Data model for Jobs table """
    id = peewee.PrimaryKeyField()
    project = peewee.ForeignKeyField(Project)
    status = peewee.IntegerField()
    name = peewee.CharField()
    description = peewee.TextField(null=True)
    log_path = peewee.CharField(null=True)
    started = peewee.DateTimeField(null=True)
    ended = peewee.DateTimeField(null=True)

class ProjectJSONEncoder(JSONEncoder):
    """ Custom json encoder for the projects class """
    #pylint: disable=E0202
    def default(self, obj): #override JSONEncoder's "default" method
        if isinstance(obj, Project):
            return dict(name=obj.name, slug=obj.slug, filepath=obj.filepath,
                        description=obj.description)
        else:
            JSONEncoder.default(self, obj)
    #pylint: enable=E0202
