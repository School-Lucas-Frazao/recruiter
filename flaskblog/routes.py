import os # This will allow us to join the picture path
import secrets # This will generate a random hex for the picture name
from PIL import Image # This will allow us to resize the picture
from flask import render_template, url_for, flash, redirect, request, abort, session # Import the Flask class, and the render template, and the main.css file
from flaskblog import app, db, bcrypt# Import the app, db, and bcrypt variables from the __init__.py file
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm # Import the RegistrationForm and LoginForm classes from forms.py
from flaskblog.models import User, Post, attendees
from flask_login import login_user, current_user, logout_user, login_required # Import the login_user function from the flask_login module

 
@app.route("/") # When we use the route decorator to tell Flask what URL should trigger our function.
@app.route("/home") # We can have multiple routes to the same function
def home(): # Name of function is just a cosmetic thing
    posts = Post.query.all()
    return render_template('home.html', posts=posts) # This reders the home.html template and gives home access to the posts variable


@app.route("/register", methods=['GET', 'POST']) # This route will accept both GET and POST requests / it routes the register page
def register():
    if current_user.is_authenticated: # This will check to see if the user is logged in
        return redirect(url_for('home')) # This will redirect the user to the home page
    form = RegistrationForm() # Create an instance of the RegistrationForm class
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # This will hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # This will create a new user with the hashed password
        db.session.add(user)
        db.session.commit() # This will commit the user to the database
        flash('Your account has been created! You are now able to log in', 'success') # This will flash a message to the user that their account was created
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form) # This reders the register.html template and gives register access to the form variable

@app.route("/login", methods=['GET', 'POST']) # This route will accept both GET and POST requests / it routes the login page
def login():
    if current_user.is_authenticated: # This will check to see if the user is logged in
        return redirect(url_for('home')) # This will redirect the user to the home page
    form = LoginForm() # Create an instance of the LoginForm class
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # This will query the database to see if the email inputed exists
        if user and bcrypt.check_password_hash(user.password, form.password.data): # This will make sure the user exits and that the password verifies with what is in the database
            login_user(user, remember=form.remember.data) # This will log the user in
            next_page = request.args.get('next') # This will get the next page that the user was trying to access before they were redirected to the login page
            return redirect(next_page) if next_page else redirect(url_for('home')) # This will redirect the user to the next page if it exists or the home page if it does not
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form) # This reders the login.html template and gives login access to the form variable

@app.route("/logout") # This route will accept GET requests / it routes the logout page
def logout():
    logout_user()
    return redirect(url_for('home')) # This will redirect the user to the home page


def save_picture(form_picture): # This function will save the picture to the database
    random_hex = secrets.token_hex(8) # This will generate a random hex for the picture name
    _, f_ext = os.path.splitext(form_picture.filename) # This will get the file extension of the picture
    picture_fn = random_hex + f_ext # This will create the picture name
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # This will create the picture path

    output_size = (125, 125) # This will set the size of the picture
    i = Image.open(form_picture) # This will open the picture
    i.thumbnail(output_size) # This will resize the picture
    i.save(picture_path) # This will save the picture to the picture path

    return picture_fn # This will return the picture name


@app.route("/account", methods=['GET', 'POST']) # This route will accept GET requests / it routes the account page
@login_required # This will make sure the user is logged in before they can access the account page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): # This will check to see if the form was submitted properly 
        if form.picture.data: # This will check to see if the user uploaded a picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file # This will update the image file
        current_user.username = form.username.data # This will update the username
        current_user.email = form.email.data  # This will update the email
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET': # This will populate the form with the current username and email
        form.username.data = current_user.username 
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # This will get the image file for the user
    return render_template('account.html', title='Account', image_file=image_file, form=form) # This reders the account.html template and gives account access to the title variable



@app.route("/post/new", methods=['GET', 'POST']) # This route will accept both GET and POST requests / it routes the new post page
@login_required # This will make sure the user is logged in before they can access the new post page
def new_post():
    form = PostForm() # Create an instance of the PostForm class
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # This will create a new post based on the form data
        db.session.add(post) # This will add the post to the database queue
        db.session.commit() # This will commit the post to the database
        flash('Your event has been created!', 'success') # This will flash a message to the user that their post was created, success is a bootstrap class
        return redirect(url_for('home')) # This will redirect the user to the home page
    return render_template('create_post.html', title='New Event', form=form, legend='New Event') # This reders the create_post.html template and gives new_post access to the title and form variables


@app.route("/post/<int:post_id>") # Posts page 
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST']) # Updates/edit a post
@login_required # This will make sure the user is logged in before they can access the update post page
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # This will get the post from the database
    if post.author != current_user: # This will check to see if the user is the author of the post
        abort(403) # If user is not the author of the post then they will get a 403 error
    form = PostForm() # This is so we can use the form to retrieve the data
    if form.validate_on_submit():
        post.title = form.title.data # updates title of post
        post.content = form.content.data # updates content of post
        db.session.commit() # There is no need for a db.session.add() because the post is already in the database
        flash('Your event has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id)) # This will redirect the user to the post page
    elif request.method == 'GET': # This will populate the form with the current post data
        form.title.data = post.title # Changes the legend and filling in the form with the current post data
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post') # legend value is used to change the title of the form

# the below file has a problem and needs to be fixed as you cannot access it

@app.route("/post/<int:post_id>/delete", methods=['POST'])  # Deletes a post
@login_required 
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # This will get the post from the database or return a 404 error
    if post.author != current_user: # This will check to see if the user is the author of the post
        abort(403) # If user is not the author of the post then they will get a 403 error
    db.session.delete(post) # This will delete the post from the database
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('home'))


# Route to sign up for an event
@app.route("/post/<int:post_id>/signup", methods=['POST'])
@login_required
def sign_up(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user not in post.attendees:
        post.attendees.append(current_user)
        db.session.commit()
        flash('You have signed up for the event!', 'success')
    else:
        flash('You are already signed up for this event!', 'info')
    return redirect(url_for('post', post_id=post.id))

# Route to un-sign up from an event
@app.route("/post/<int:post_id>/unsignup", methods=['POST'])
@login_required
def un_sign_up(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.attendees:
        post.attendees.remove(current_user)
        db.session.commit()
        flash('You have un-signed up from the event!', 'success')
    else:
        flash('You are not signed up for this event!', 'info')
    return redirect(url_for('post', post_id=post.id))


@app.route("/post/<int:post_id>/attend/<int:user_id>")
@login_required
def attend_event(post_id, user_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)
    if user in post.attendees:
        post.attendees.remove(user)
        user.service_hours += 1  # Add one hour to the user's service hours
        db.session.commit()
        flash('Attendance marked and service hour added.', 'success')
    else:
        flash('User is not signed up for this event.', 'danger')
    return redirect(url_for('post', post_id=post.id))


@app.route("/user/<int:user_id>/service_hours")
@login_required
def user_service_hours(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('service_hours.html', user=user)



