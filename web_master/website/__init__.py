from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

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

    from .models import User, Entry, Location, Route

    login_manager = LoginManager()
    login_manager.login_view = 'views.landing_page'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)
    create_superuser(User, app)
    return app


def create_database(app):
    if not path.exists('website/' + "tenerife"):
        db.create_all(app=app)
        print("Successfully created DB")


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
