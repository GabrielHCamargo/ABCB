from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
app.config.from_object('config')
CORS(app, expose_headers=["Content-Disposition"])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import imports, tables, forms, default, clients, exports
from app.controllers import default, clients, exports, imports