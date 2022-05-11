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
    name = db.Column(db.String(30))  # day and poi number
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
    date = db.Column(db.DateTime(timezone=True), default=func.now())
