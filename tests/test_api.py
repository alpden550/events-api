import pytest
from flask import request

from events_api.extensions import db
from events_api.models import Event, Location
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
            Event.create(title='Django', location=locations[1], event_type='GAME')

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.session.query(Location).delete()
            db.session.query(Event).delete()
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
