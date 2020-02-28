from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from events_api.admin import AdminView

db = SQLAlchemy()
login = LoginManager()
admin = Admin(index_view=AdminView(), name='EVENTS CRM')
