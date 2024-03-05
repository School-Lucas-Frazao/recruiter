from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object(Config) # This is a secret key that is used to protect the application from attacks like CSRF
db = SQLAlchemy(app) # This is the database instance

from jobrecruiter import routes, models # This is the routes file that will be used to run the app