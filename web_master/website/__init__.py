from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv, listdir
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import json
import pandas as pd
import datetime

db = SQLAlchemy()

def create_app(conn_string):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY', "SuperSecretKeyOfDoomAndDarkness")
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # max upload size = 5mb
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Entry, Location, Route, Vegetation

    login_manager = LoginManager()
    login_manager.login_view = 'views.landing_page'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app, Location, Route, Vegetation)
    create_superuser(User, app)
    return app


def create_database(app, Location, Route, Vegetation):
    if not path.exists('website/' + "tenerife"):
        db.create_all(app=app)
        import_locations(Location, app)
        import_routes(Route, app)
        import_vegetation(Vegetation, app)
        print("Successfully created DB")


def import_locations(Location, app):
    with app.app_context():
        if not Location.query.first():
            directory = '../data/gps/pois/'
            for file in listdir(directory):
                if file.endswith('.geojson'):
                    with open(directory + file) as f:
                        data = json.load(f)
                    for feature in data["features"]:
                        new_location = Location(name=(data["name"]+'_'+feature['properties']['name']),
                                                elevation=feature['properties']['ele'],
                                                category=feature['properties']['cmt'],  # the tag e.g. -Stone-
                                                geojson=json.dumps(feature["geometry"]),
                                                date=feature['properties']['time'])
                        db.session.add(new_location)
                        db.session.commit()


def import_routes(Route, app):
    with app.app_context():
        if not Route.query.first():
            directory = '../data/gps/tracks/'
            for file in listdir(directory):
                if file.endswith('.geojson'):
                    with open(directory + file) as f:
                        data = json.load(f)
                    for feature in data["features"]:
                        new_route = Route(name=feature['properties']['name'],
                                          geojson=json.dumps(feature["geometry"]))
                        db.session.add(new_route)
                        db.session.commit()


def import_vegetation(Vegetation, app):
    with app.app_context():
        if not Vegetation.query.first():
            directory = '../data/plants/'
            for file in listdir(directory):
                if file.endswith('.csv'):
                    df = pd.read_csv(directory+file, sep=';', header=0)
                    df = df.reset_index()
                    for index, row in df.iterrows():
                        imagelist = row['images'].splitlines(0)
                        imagedict = {}
                        for element in imagelist:
                            data = element.split()
                            imagedict[data[1][1:-1]] = data[0]
                        coordinateslist = [float(row['longitude'].replace(",", ".")), float(row['latitude'].replace(",", "."))]
                        jsondict = {'type': 'Point', 'coordinates': coordinateslist}

                        new_vegetation = Vegetation(
                            id=row['id'],
                            geojson=json.dumps(jsondict),
                            url=row['URL'],
                            author=row['author'],
                            author_url=row['author URL'],
                            date=datetime.datetime.fromtimestamp(row['date observed (timestamp milliseconds)'] / 1000.0, tz=datetime.timezone.utc),
                            project=row['project'],
                            current_name=row['current name'],
                            original_name=row['original name'],
                            family=row['family'],
                            valid=row['valid'],
                            license=row['license'],
                            comments=row['comments'],
                            image_bark=imagedict.get('bark'),
                            image_fruit=imagedict.get('fruit'),
                            image_habit=imagedict.get('habit'),
                            image_leaf=imagedict.get('leaf'),
                            image_flower=imagedict.get('flower'),
                            zone=row['zone'])
                        db.session.add(new_vegetation)
                        db.session.commit()


def create_superuser(User, app):
    """Automatically create a superuser which has special privileges."""
    with app.app_context():
        superuser_pw = getenv('SUPERUSER_PW', "Valid12!")
        # check if already in db
        if not User.query.filter_by(username="Jochen Stier").first():
            superuser = User(
                username="Jochen Stier",
                vorname="Jochen",
                name="Stier",
                password=generate_password_hash(superuser_pw, method="sha256"),
                superuser=True
            )
            db.session.add(superuser)
            db.session.commit()
