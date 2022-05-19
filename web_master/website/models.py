from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
"""Hier liegen alle Datenbankschema, heißt Tabellen auf die zugegriffen werden kann."""


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


class Location(db.Model):
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


class Entry(db.Model):
    """Entries -> Extra photos for location with image, title and description."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    text = db.Column(db.String(500))
    category = db.Column(db.String(30))
    image = db.Column(db.LargeBinary)
    image_data_type = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))


class Route(db.Model):
    """Travel Routes per day"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # day
    geojson = db.Column(db.String())


class Vegetation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    author = db.Column(db.String(30))
    author_url = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    project = db.Column(db.String(30))
    current_name = db.Column(db.String(75))
    original_name = db.Column(db.String(75))
    family = db.Column(db.String(30))
    valid = db.Column(db.Boolean)
    license = db.Column(db.String(30))
    geojson = db.Column(db.String())
    comments = db.Column(db.String(500))
    image_bark = db.Column(db.String(500))
    image_data_type_bark = db.Column(db.String(10))
    image_fruit = db.Column(db.String(500))
    image_data_type_fruit = db.Column(db.String(10))
    image_habit = db.Column(db.String(500))
    image_data_type_habit = db.Column(db.String(10))
    image_leaf = db.Column(db.String(500))
    image_data_type_leaf = db.Column(db.String(10))
    image_flower = db.Column(db.String(500))
    image_data_type_flower = db.Column(db.String(10))
    zone = db.Column(db.String(50))
