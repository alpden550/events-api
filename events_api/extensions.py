from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from events_api.admin import AdminView

db = SQLAlchemy()
login = LoginManager()
admin = Admin(index_view=AdminView(), name='EVENTS CRM')
csrf = CSRFProtect()
login = LoginManager()

login.login_view = 'admin.login'
login.login_message = 'Авторизуйтесь для доступа к CRM'
