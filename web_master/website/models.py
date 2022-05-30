from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect

"""Hier liegen alle Datenbankschema, heißt Tabellen auf die zugegriffen werden kann."""


class Serializer(object):
    def serialize(self):
        l = {}
        for key in inspect(self).attrs.keys():
            value = getattr(self, key)
            if isinstance(value, bytes):
                value = str(value, encoding='utf-8')
            l[key] = value
        return l

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class User(db.Model, UserMixin):
    """Account Information for all Users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    vorname = db.Column(db.String(30))
    name = db.Column(db.String(30))
    password = db.Column(db.String(100))
    superuser = db.Column(db.Boolean, default=False)
    image = db.Column(db.LargeBinary)
    image_data_type = db.Column(db.String(10))
    entries = db.relationship('Entry')


class Location(db.Model, Serializer):
    """Locations on the map"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # day and poi number
    caption = db.Column(db.String(50))
    text = db.Column(db.String(500))
    elevation = db.Column(db.Float)
    category = db.Column(db.String(30))  # the tag e.g. -Stone-
    geojson = db.Column(db.String())
    image = db.Column(db.LargeBinary)
    image_data_type = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # todo: these should not use default, but their actual date
    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Entry(db.Model):
    """Entries -> Extra photos for location with image, title and description."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(18))
    text = db.Column(db.String(500))
    category = db.Column(db.String(30))
    image = db.Column(db.LargeBinary)
    image_data_type = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Route(db.Model):
    """Travel Routes per day"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # day
    geojson = db.Column(db.String())
    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Vegetation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    author = db.Column(db.String(30))
    date = db.Column(db.Date(), default=func.now())
    current_name = db.Column(db.String(75))
    family = db.Column(db.String(30))
    geojson = db.Column(db.String())
    image_bark = db.Column(db.String(500))
    image_fruit = db.Column(db.String(500))
    image_habit = db.Column(db.String(500))
    image_leaf = db.Column(db.String(500))
    image_flower = db.Column(db.String(500))
    zone = db.Column(db.String(50))
    def serialize(self):
        d = Serializer.serialize(self)
        return d

