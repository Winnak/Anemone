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
    path = peewee.CharField(null=False)
    description = peewee.TextField(null=True)
    # scheduletype = peewee.BooleanField(default=True, null=True) #future version might have different options.
    output = peewee.CharField()
    created_at = peewee.DateTimeField()

class Job(BaseModel):
    """ Data model for Jobs table """
    id = peewee.PrimaryKeyField()
    project = peewee.ForeignKeyField(Project)
    result = peewee.IntegerField(default=0) # 1: success, 2: warning, 3: error
    active = peewee.BooleanField(default=False)
    name = peewee.CharField()
    description = peewee.TextField(null=True)
    log_path = peewee.CharField(null=True)
    path = peewee.CharField(null=True)
    started = peewee.DateTimeField(null=True)
    ended = peewee.DateTimeField(null=True)
    def get_status(self):
        """ Returns the current status id """
        status = 0
        if self.started is not None:
            if self.active:
                status = 4
            else:
                status = 5
            if self.ended is not None:
                status = int(self.result)
        return status

class ProjectJSONEncoder(JSONEncoder):
    """ Custom json encoder for the projects class """
    #pylint: disable=E0202
    def default(self, obj): #override JSONEncoder's "default" method
        if isinstance(obj, Project):
            return dict(name=obj.name, slug=obj.slug, path=obj.path,
                        description=obj.description)
        else:
            JSONEncoder.default(self, obj)
    #pylint: enable=E0202
