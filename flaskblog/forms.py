# Description: This file will define the forms we will use in our application
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed #import the FileField and FileAllowed classes from the flask_wtf.file module
from flask_login import current_user #import the current user variable from the flask_login module
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField #import the fields we want to use
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError #import the validators we want to use
from flaskblog.models import User #import the User class from the models file

class RegistrationForm(FlaskForm): #This class will define our registration form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) #creates a username field in the form that requires data and has a length between 2 and 20 characters
    email = StringField('Email', validators=[DataRequired(), Email()]) #creates an email field in the form that requires data and is a valid emai
    password = PasswordField('Password', validators=[DataRequired()]) #creates a password field in the form that requires data
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) #creates a confirm password field in the form that requires data and is equal to the password field
    submit = SubmitField('Sign Up') #creates a submit field in the form that is a submit button

    def validate_username(self, username): #This function will validate the username and make sure it is not already in use
        user = User.query.filter_by(username=username.data).first() #query the database to see if the username is already in use
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email): #This function will validate the email and make sure it is not already in use
        user = User.query.filter_by(email=email.data).first() #query the database to see if the email is already in use
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm): #This class will define our login form
    email = StringField('Email', validators=[DataRequired(), Email()]) #creates an email field in the form that requires data and is a valid emai
    password = PasswordField('Password', validators=[DataRequired()]) #creates a password field in the form that requires data
    remember = BooleanField('Remember Me') #creates a remember me field in the form that is a checkbox using a cookie
    submit = SubmitField('Login') #creates a submit field in the form that is a submit button


class UpdateAccountForm(FlaskForm): #This class will define our registration form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) #creates a username field in the form that requires data and has a length between 2 and 20 characters
    email = StringField('Email', validators=[DataRequired(), Email()]) #creates an email field in the form that requires data and is a valid emai

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) #creates a picture field in the form that allows jpg and png files

    submit = SubmitField('Update') #creates a submit field in the form that is a submit button

    def validate_username(self, username): #This function will validate the username and make sure it is not already in use
        if username.data != current_user.username: #This will check to see if the username is different than the current username
            user = User.query.filter_by(username=username.data).first() #query the database to see if the username is already in use
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email): #This function will validate the email and make sure it is not already in use
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() #query the database to see if the email is already in use
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            

class PostForm(FlaskForm): #This class will define our post form, it imports from FlaskForm
    title = StringField('Name', validators=[DataRequired()]) #creates a title field in the form that requires data
    content = TextAreaField('Description', validators=[DataRequired()]) #creates a content field in the form that requires data
    submit = SubmitField('Post') #creates a submit field in the form that is a submit button



#noah's test comment