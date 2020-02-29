import json

import pytest
from flask import request

from events_api.extensions import db
from events_api.models import Event, Location, Participant, Enrollment
from tests.conftest import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestApi:

    @classmethod
    def setup_class(cls):
        with app.app_context():
            Location.create(title='Москва')
            Location.create(title='Спб')
            locations = Location.query.all()
            Event.create(title='Flask', location=locations[0])
            Event.create(title='Django', location=locations[1], event_type='GAME', seats=1)
            Participant.create(name='Name', email='test@gmail.com', password='qwerty')
            Participant.create(name='Another Name', email='another@gmail.com', password='qwerty')

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.drop_all(app=app)
            db.session.commit()

    def test_api_page(self, client):
        response = client.get('/api/')
        assert response.status_code == 200

    def test_locations(self, client):
        response = client.get('/api/locations/')
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_events(self, client):
        response = client.get('/api/events/')
        assert response.content_type == 'application/json'
        assert len(response.json) == 2
        assert response.status_code == 200

    def test_event_with_location(self, client):
        response = client.get('/api/events/?location=москва')
        assert response.content_type == 'application/json'
        assert len(response.json) == 1

    def test_event_with_eventtype(self, client):
        response = client.get('/api/events/?eventtype=hackaton')
        assert response.content_type == 'application/json'
        assert len(response.json) == 1

    def test_register_enrollment_wrong_email(self, client):
        json_data = json.dumps({'email': 'test@test.com'})
        response = client.post(
            '/api/enrollments/1',
            data=json_data,
            content_type='application/json',
        )
        assert response.status_code == 400
        assert 'error' in response.json.get('status')

    def test_register_enrollment_correct_email(self, client):
        json_data = json.dumps({'email': 'test@gmail.com'})
        response = client.post(
            '/api/enrollments/1',
            data=json_data,
            content_type='application/json',
        )
        assert response.status_code == 201
        assert 'success' in response.json.get('status')

    def test_register_enrollment_wrong_event(self, client):
        response = client.post(
            '/api/enrollments/10',
            content_type='application/json',
        )
        assert response.status_code == 400
        assert 'error' in response.json.get('status')

    def test_register_enrollment_no_seats(self, client):
        json_data = json.dumps({'email': 'test@gmail.com'})
        response = client.post(
            '/api/enrollments/2',
            data=json_data,
            content_type='application/json',
        )
        another_response = client.post(
            '/api/enrollments/2',
            data=json.dumps({'email': 'another@gmail.com'}),
            content_type='application/json',
        )
        assert another_response.status_code == 500
        assert 'error' in another_response.json.get('status')

    def test_register_enrollment_user_already_exist(self, client):
        json_data = json.dumps({'email': 'test@gmail.com'})
        response = client.post(
            '/api/enrollments/1',
            data=json_data,
            content_type='application/json',
        )
        another_response = client.post(
            '/api/enrollments/1',
            data=json.dumps({'email': 'test@gmail.com'}),
            content_type='application/json',
        )
        assert another_response.status_code == 500
        assert another_response.json.get('status') == 'error, user already enrrolled'
