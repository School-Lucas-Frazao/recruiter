from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c7b9d1d86846390b91fa1ef4d27172d0' # This is a secret key that is used to protect the application from attacks like CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # This is the location of our database
db = SQLAlchemy(app) # This is the database instance

from jobrecruiter import routes, models # This is the routes file that will be used to run the app