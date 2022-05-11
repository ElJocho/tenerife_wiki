from ..models import Entry
from ..views import db


def get_entries(l_id):
    return db.session.query(Entry).filter(Entry.location_id == l_id).all()
