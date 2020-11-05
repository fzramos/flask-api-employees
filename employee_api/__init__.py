from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) # Ingest data via models
migrate = Migrate(app, db) # Ingest data via models
ma = Marshmallow(app) # Digest data from our models

login_manager = LoginManager(app)

from employee_api import models, routes