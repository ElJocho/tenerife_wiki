import json

from flask import Blueprint, jsonify, request, render_template, Response
from flask_login import current_user, login_required
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import set_attribute, flag_modified
from sqlalchemy import update
from . import db
from .models import Location, Route, User, Entry
from .python_utils.files import allowed_file, ALLOWED_IMAGE_EXTENSIONS, cleanup_image

api = Blueprint("api", __name__)


@api.route('/get_locations', methods=["GET"])
def get_locations():
    return jsonify([location.serialize() for location in Location.query.all()])


@api.route('/get_routes', methods=["GET"])
def get_routes():
    return jsonify([route.serialize() for route in Route.query.all()])


@api.route("/get_entries", methods=["GET"])
def get_entries():
    location_id = request.args.get('l_id')
    entries = db.session.query(Entry).filter(Entry.location_id == location_id).all()

    entry_list = []
    for entry in entries:
        inner_entry = entry.serialize()
        u = User.query.filter_by(id=entry.user_id).first()
        inner_entry["user_image"] = u.image
        inner_entry["user_image_data_type"] = u.image_data_type
        entry_list.append(inner_entry)
    return json.dumps(entry_list, default=str)


@login_required
@api.route("/edit_location", methods=["POST"])
def edit_location():
    data = request.form
    caption = data.get("caption")
    text = data.get("text")
    location_id = request.args.get('l_id')
    location_image = request.files.get("location_image")
    if location_image:
        if location_image.filename != "" and allowed_file(location_image.filename,
                                                         ALLOWED_IMAGE_EXTENSIONS):
            image, image_data_type = cleanup_image(location_image)
            update_sql = update(Location).where(Location.id == location_id).values(
                image=image,
                image_data_type=image_data_type
            )
            db.get_engine().execute(update_sql)
            db.session.commit()

    if caption:
        update_sql = update(Location).where(Location.id == location_id).values(caption=caption)
        db.get_engine().execute(update_sql)
        db.session.commit()

    if text:
        update_sql = update(Location).where(Location.id == location_id).values(text=text)
        db.get_engine().execute(update_sql)
        db.session.commit()

    return render_template(
        "home.html",
        user=current_user,
        locations=Location.query.all(),
        routes=Route.query.all()
    )


@login_required
@api.route("/new_entry", methods=["POST"])
def new_entry():
    data = request.form
    entry_title = data.get("entry_title")
    entry_text = data.get("entry_text")
    entry_category = data.get("entry_category")
    location_id = request.args.get('l_id')
    entry_image = request.files.get("entryImage")

    if entry_image.filename != "" and allowed_file(entry_image.filename,
                                                  ALLOWED_IMAGE_EXTENSIONS):
        image, image_data_type = cleanup_image(entry_image)

        entry = Entry(
            title=entry_title, text=entry_text,
            category=entry_category,
            user_id=current_user.id, image=image,
            image_data_type=image_data_type,
            location_id=location_id
        )
        db.session.add(entry)
        db.session.commit()
        return json.dumps(entry.serialize(), default=str)
    else:
        return Response(
            "Invalid Image Data Type, allowed are: .pdf, .png, .jpg, .jpeg.",
            status=400,
        )
