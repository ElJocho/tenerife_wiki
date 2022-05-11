import json
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Entry, User, Location, Route
from . import db
from .python_utils.files import cleanup_image, allowed_file, ALLOWED_IMAGE_EXTENSIONS
from .python_utils.query import get_entries
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


@views.route("/location", methods=["GET"])
def location_site():
    location_id = request.args.get('l_id')
    location = Location.query.get(location_id)
    entries = get_entries(location_id)
    for entry in entries:
        u = User.query.filter_by(id=entry.user_id).first()
        entry.user_image = u.image
        entry.user_image_data_type = u.image_data_type
    return render_template(
        "Location.html",
        user=current_user,
        location=location,
        entries=entries,
    )

@login_required
@views.route("/new-entry", methods=["POST"])
def new_idea_l1():
    data = request.form
    entry_title = data.get("title")
    entry_text = data.get("text")
    entry_category = data.get("category")
    entry_location = data.get("location_id")
    entry_image = request.files.get("ideaImage")

    if entry_image.filename != "" and allowed_file(entry_image.filename,
                                                  ALLOWED_IMAGE_EXTENSIONS):
        image, image_data_type = cleanup_image(entry_image)

        entry = Entry(
            title=entry_title, text=entry_text,
            category=entry_category,
            user_id=current_user.id, image=image,
            image_data_type=image_data_type,
            location_id=entry_location
        )
        db.session.add(entry)
        db.session.commit()
        return json.dumps({"id": entry.id})
