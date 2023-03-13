from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.abspath('./properties/')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, models

Property = models.Property
