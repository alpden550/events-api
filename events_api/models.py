from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy_utils import ChoiceType, EmailType
from werkzeug.security import check_password_hash, generate_password_hash

from events_api.extensions import db, login


class BaseMixin:
    """
    A mixin that adds a surrogate integer 'primary key' column named `id`
    to any declarative-mapped class and other usefull stuff.
    """

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():  # noqa:WPS110
            setattr(self, attr, value)
        return self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:  # pragma: no cover
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
            else:
                return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password, password)


events_participants = db.Table(
    'events_participants',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id')),
)


class User(UserMixin, BaseMixin, db.Model):
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'


class Event(BaseMixin, db.Model):
    EVENT_TYPES = [
        ('HACKATON', 'Хакатон'),
        ('WORKSHOP', 'Воркшоп'),
        ('GAME', 'Игра'),
    ]
    CATEGORY_TYPES = [
        ('PYTHON', 'Python'),
        ('ML', 'ML'),
        ('PROJECT MANAGEMENT', 'Управление проектами'),
    ]

    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    event_type = db.Column(ChoiceType(EVENT_TYPES), default='HACKATON')
    category = db.Column(ChoiceType(CATEGORY_TYPES), default='PYTHON')
    address = db.Column(db.String(150))
    seats = db.Column(db.Integer, default=10)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    participants = db.relationship(
        'Participant', secondary='events_participants', back_populates='events', lazy='joined',
    )
    enrollments = db.relationship('Enrollment', back_populates='event', lazy='joined')
    location = db.relationship('Location', back_populates='events', lazy='joined')

    def __repr__(self):
        return f'<Event {self.title}>'


class Participant(BaseMixin, db.Model):
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(EmailType, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    picture = db.Column(db.String(100))
    location = db.Column(db.String(30))
    about = db.Column(db.String(300))

    events = db.relationship(
        'Event', secondary='events_participants', back_populates='participants', lazy='joined',
    )
    enrollments = db.relationship('Enrollment', back_populates='participant', lazy='joined')

    def __repr__(self):
        return f'<Participant {self.name}>'


class Enrollment(BaseMixin, db.Model):
    registrated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    participant = db.relationship('Participant', back_populates='enrollments')
    event = db.relationship('Event', back_populates='enrollments')

    def __repr__(self):
        return f'<Enrollment {self.id}>'


class Location(BaseMixin, db.Model):
    title = db.Column(db.String(20))
    location_type = db.Column(db.String(10), default='online')
    events = db.relationship('Event', back_populates='location')

    def __repr__(self):
        return f'<Location {self.title}>'


@event.listens_for(Participant.password, 'set', retval=True)
def hash_partisipant_password(target, password, *args):
    return generate_password_hash(password)


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, password, *args):
    return generate_password_hash(password)


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))
