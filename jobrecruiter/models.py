from datetime import datetime
from jobrecruiter import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader # Login manager setup
def load_user(user_id): 
    return User.query.get(int(user_id)) 


class User(db.Model, UserMixin):  # This defines our database
    id = db.Column(db.Integer, primary_key=True) # unique key for each user
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    applications = db.relationship('Application', backref='author', lazy=True) # This is a relationship between the user and the application

    def __repr__(self): # This is a magic method that returns a string when we print the object
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Application(db.Model): # This is a class that represents an application
    id = db.Column(db.Integer, primary_key=True) # unique key for each application
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # This is the date the application was posted
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # This is a foreign key that links the application to the user

    def __repr__(self): # This is a magic method that returns a string when we print the object
        return f"Application('{self.title}', '{self.date_posted}')"