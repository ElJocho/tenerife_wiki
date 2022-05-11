from flask import Blueprint, jsonify

from web_master.website.models import Location, Route

api = Blueprint("api", __name__)


@api.route('/get_locations', methods=["GET"])
def get_locations():
    return jsonify(Location.query.all())


@api.route('/get_routes', methods=["GET"])
def get_routes():
    return jsonify(Route.query.all())
