from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Import the SQLAlchemy class
from flask_bcrypt import Bcrypt # Import the Bcrypt class
from flask_login import LoginManager # Import the LoginManager class

app = Flask(__name__) # Create an instance of the class for our use
app.config['SECRET_KEY'] = 'a0a1175b0fe2a4e436e881d9d5fcbe26' # This is a secret key that is used to protect against modifying cookies and cross-site request forgery attacks when using forms
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # This is the location of our database
db = SQLAlchemy(app) # Create an instance of the SQLAlchemy database
bcrypt = Bcrypt(app) # Create an instance of the Bcrypt class
login_manager = LoginManager(app) # Create an instance of the LoginManager class
login_manager.login_view = 'login' # This will tell the login manager where the login route is located. This is so that it can redirect the user to the login page if they are not logged in and try to access a page that requires them to be logged in
login_manager.login_message_category = 'info' # This will make the message that is flashed to the user when they try to access a page that requires them to be logged in be blue

from flaskblog import routes # Cannot be at the top of the file because of circular imports
