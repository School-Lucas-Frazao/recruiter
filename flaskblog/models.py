from datetime import datetime # Import the datetime class from the datetime module
from flaskblog import db, login_manager #imports database from flaskblog.py and the login manager with will be used to manage the user logins
from flask_login import UserMixin # Import the UserMixin class from the flask_login module. This will give us the attributes and methods needed for user management

@login_manager.user_loader # This decorator will allow us to load the user from the database
def load_user(user_id): # This function will load the user from the database for use with the login manager
    return User.query.get(int(user_id)) # This will return the user from the database

attendees = db.Table('attendees',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class User(db.Model, UserMixin): # This class will define our user table
    id = db.Column(db.Integer, primary_key=True) # This is the id column of the table
    username = db.Column(db.String(20), unique=True, nullable=False) # This is the username column of the table, the nullable=False means that it can't be null, you need a username
    email = db.Column(db.String(120), unique=True, nullable=False) # This is the email column of the table
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # This is the image file column of the table, it is for the user's profile picture
    password = db.Column(db.String(60), nullable=False) # This is the password column of the table
    posts = db.relationship('Post', backref='author', lazy=True) # This is a relationship between the user and the post table, it is a one to many relationship, one user can have many posts, 
    #the backref is similar to adding another column to the post table, it will allow us to get the user who created the post, the lazy argument defines when SQLAlchemy loads the data from the database.
    service_hours = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self): # This is how the object is printed
        return f"User('{self.username}', '{self.email}', '{self.image_file}')" # This is what is printed
    

class Post(db.Model): # This class will define our post table
    id = db.Column(db.Integer, primary_key=True) # This is the id column of the table
    title = db.Column(db.String(100), nullable=False) # This is the title column of the table
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # This is the date posted column of the table, it is the date the post was created
    content = db.Column(db.Text, nullable=False) # This is the content column of the table, it is the content of the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # This is the user id column of the table, it is the id of the user who created the post
    attendees = db.relationship('User', secondary=attendees, backref=db.backref('attending', lazy='dynamic'))

    def __repr__(self): 
        return f"Post('{self.title}', '{self.date_posted}')"