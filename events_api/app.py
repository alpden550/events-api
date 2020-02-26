import os

from flask import Flask

from events_api.blueprints.main import main_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'production')

    app = Flask(__name__)

    app.register_blueprint(main_bp)

    return app
