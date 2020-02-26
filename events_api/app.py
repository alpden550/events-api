import os

from flask import Flask

from events_api.blueprints.api import api_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'production')

    app = Flask(__name__)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
