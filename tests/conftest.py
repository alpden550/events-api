from events_api import create_app
from events_api.extensions import db

app = create_app(config_name='testing')
db.create_all(app=app)
