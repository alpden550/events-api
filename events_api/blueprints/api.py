from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from events_api.models import Event, Location
from events_api.schema_models import EventSchema, LocationSchema

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index():
    return 'Hello, api!'


@api_bp.route('/locations/', methods=['GET'])
def get_locations():
    locations = Location.query
    schema = LocationSchema(many=True)
    locations_json = schema.dump(locations)
    return jsonify(locations_json), 200


@api_bp.route('/events/', methods=['GET'])
def get_events():
    location = request.args.get('location')
    eventtype = request.args.get('eventtype')
    events = Event.query

    if location:
        events = events.join(Event.location).filter_by(title=location.capitalize())
    if eventtype:
        events = events.filter(Event.event_type == eventtype.upper())

    schema = EventSchema(many=True)
    events_json = schema.dump(events)
    return jsonify(events_json), 200


@api_bp.route('/enrollments/<int:eventid>', methods=['GET'])
def get_enrollment(eventid):
    return jsonify({'status': 'success'})


@api_bp.route('/enrollments/<int:eventid>', methods=['DELETE'])
def delete_enrollment(eventid):
    return jsonify({'delete': 'success'})


@api_bp.route('/register/', methods=['POST'])
def register():
    return jsonify({'status': 'ok', 'id': 1})


@api_bp.route('/auth', methods=['POST'])
def authorize():
    return jsonify({'status': 'success', 'key': 111111111})


@api_bp.route('/profile/<int:profileid>', methods=['GET'])
def profile(profileid):
    return jsonify({'id': 1, 'picture': '', 'city': 'nsk', 'about': '', 'enrollments': []})
