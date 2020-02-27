import os

import click
from flask import Flask

from events_api.blueprints.api import api_bp
from events_api.extensions import db
from events_api.settings import config
from events_api.models import User


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'production')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(api_bp, url_prefix='/api')
    register_extensions(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_commands(app):
    @app.cli.command()
    def init():
        """Create empty database."""
        db.drop_all()
        db.create_all()
        # Event.query.all()
        click.echo('Initialized empty database.')

    @app.cli.command()
    @click.option('-n', '--name', default='admin', help='Username for admin')
    @click.option('-e', '--email', default='admin@gmail.com', help='Email for admin')
    @click.option('-p', '--password', default='1111', help='Password for admin')
    def superuser(name, email, password):
        """Create default admin."""
        admin = User(username=name, email=email, password=password)
        db.session.add(admin)
        db.session.commit()
        click.echo('Default admin was created.')
