import json
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Entry, User, Location, Route
from . import db
from .python_utils.files import cleanup_image, allowed_file, ALLOWED_IMAGE_EXTENSIONS
import json

"""Aktuell Homepage und ein weiterer Backend-Schnittpunkt"""

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html", user=current_user)


@views.route('/home', methods=["GET", "POST"])
def home():
    return render_template(
        "home.html",
        user=current_user,
        locations=Location.query.all(),
        routes=Route.query.all()
    )


@views.route('/impressum', methods=["GET"])
def impressum():
    return render_template(
        "impressum.html",
        user=current_user,
        locations=Location.query.all(),
        routes=Route.query.all()
    )


@login_required
@views.route('/delete-entry', methods=["POST"])
def delete_entry():
    entry_data = json.loads(request.data)
    id = entry_data["id"]
    target = Entry.query.get(id)
    if target:
        if target.user_id == current_user.id or current_user.superuser is True:
            db.session.delete(target)
            db.session.commit()
    return '', 204  # flask needs return, this one is empty
