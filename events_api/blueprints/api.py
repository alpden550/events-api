from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index():
    return 'Hello, api!'


@api_bp.route('/locations/', methods=['GET'])
def get_locations():
    return jsonify([])


@api_bp.route('/events/', methods=['GET'])
def get_events():
    return jsonify([])


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
