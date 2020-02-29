from flask import Blueprint, jsonify, request

from events_api.extensions import csrf, db
from events_api.models import Enrollment, Event, Location, Participant
from events_api.schema_models import EventSchema, LocationSchema, ParticipantSchema

api_bp = Blueprint('api', __name__)
csrf.exempt(api_bp)


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


@api_bp.route('/enrollments/<int:eventid>', methods=['POST'])
def get_enrollment(eventid):
    event = Event.query.get(eventid)
    if len(event.enrollments) > event.seats:
        return jsonify({'status': 'error, not seats'}), 500

    participant = Participant.query.filter_by(email=request.json.get('email')).first()
    if participant is None:
        return jsonify({'status': 'error, email does not exist'}), 400
    if participant.id in (participant.id for participant in event.participants):
        return jsonify({'status': 'error, user already enrrolled'}), 500

    enrollment = Enrollment.create(event=event, participant=participant)
    event.participants.append(participant)
    db.session.add(event)
    db.session.commit()
    return (
        jsonify({'status': 'success'}),
        201,
        {'Location': f'/enrollments/{enrollment.id}'},
    )


@api_bp.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if enrollment is None:
        return jsonify({'status': 'error, enrollment does not exist'}), 400
    enrollment.delete()
    return jsonify({'delete': 'success'}), 201


@api_bp.route('/register/', methods=['POST'])
def register():
    participant_json = request.json
    participant_fields = (
        participant_json.get('name'),
        participant_json.get('email'),
        participant_json.get('password'),
        participant_json.get('location'),
        participant_json.get('about'),
    )
    participant = Participant.query.filter_by(email=participant_json.get('email')).first()

    if participant is not None:
        return jsonify({'status': 'error, participant already exist'}), 500
    if not all(participant_fields):
        return jsonify({'status': 'error, not all required fields are'}), 500

    new_participant = Participant.create(**participant_json)
    return jsonify(participant_json), 201, {'Location': f'/participant/{new_participant.id}'}


@api_bp.route('/auth/', methods=['POST'])
def authorize():
    participant_json = request.json
    participant_fields = (
        participant_json.get('email'),
        participant_json.get('password'),
    )
    participant = Participant.query.filter_by(email=participant_json.get('email')).first()
    schema = ParticipantSchema()
    participant_schema = schema.dump(participant)

    if not all(participant_fields):
        return jsonify({'status': 'error, not all required fields are'}), 400
    if participant is None:
        return jsonify({'status': 'error, participant does not exist'}), 400
    if not participant.validate_password(participant_json.get('password')):
        return jsonify({'status': 'error, participant password not right'}), 400
    return jsonify(participant_schema), 201, {'Location': f'/participant/{participant.id}'}


@api_bp.route('/profile/<int:profileid>', methods=['GET'])
def profile(profileid):
    return jsonify({'id': 1, 'picture': '', 'city': 'nsk', 'about': '', 'enrollments': []})
