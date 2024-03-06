import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from jobrecruiter import app, db, bcrypt
from jobrecruiter.forms import RegistrationForm, LoginForm, UpdateAccountForm, ApplicationForm, ResumeForm
from jobrecruiter.models import User, Application, Resume
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/home") # This is a decorator
def home():
    applications = Application.query.all()
    return render_template('home.html', applications=applications)

@app.route("/homeApplicant") # This is a decorator
def homeApplicant(): #applicant home page
    applications = Application.query.all()
    return render_template('homeApplicant.html', applications=applications)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 'applicant':
                return redirect(url_for('homeApplicant'))
            elif user.role == 'employer':
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/about") 
def about():
    return render_template('about.html', title='About') # renders about.html template and passes title variable





@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #Makes sure picture name is random and does not conflic with other pictures' names
    _, f_ext = os.path.splitext(form_picture.filename) 
    picture_fn = random_hex + f_ext #concatenates the random hex with the file extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #saves the picture to the profile_pics folder

    output_size = (125, 125) #resizes the picture to 125x125
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #saves the picture to the picture path

    return picture_fn


@app.route("/register", methods=['GET', 'POST']) # This is a decorator
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit(): #if the submit is valid, flash the below message
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/my_resume")
def my_resume():
    form = ResumeForm()
    if form.validate_on_submit(): #if the submit is valid, flash the below message
        resume = Resume(work_history=form.work_history.data, education=form.education.data, contact_info=form.contact_info.data)
        db.session.add(resume)
        db.session.commit()
        flash('Resume Updated!', 'success')
        return redirect(url_for('homeApplicant'))
    return render_template('my_resume.html', title='My Resume', form=form, legend='Update Application')




@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #saves the picture to the user's profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() #commit the changes to the database
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account')) 
    elif request.method == 'GET':
        form.username.data = current_user.username #populate the form with the current user's username and email
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form = form)



@app.route("/application/new", methods=['GET', 'POST'])
@login_required
def new_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(application)
        db.session.commit()
        flash('Your application has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_application.html', title='New Application', form=form, legend='New Application')


@app.route("/application/<int:application_id>")
def application(application_id):
    application = Application.query.get_or_404(application_id)
    return render_template('application.html', title=application.title, application=application)


@app.route("/application/<int:application_id>/update", methods=['GET', 'POST'])
@login_required
def update_application(application_id):
    application = Application.query.get_or_404(application_id)
    if application.author != current_user:
        abort(403)
    form = ApplicationForm()
    if form.validate_on_submit():
        application.title = form.title.data
        application.content = form.content.data
        db.session.commit()
        flash('Your application has been updated!', 'success')
        return redirect(url_for('application', application_id=application.id))
    elif request.method == 'GET':
        form.title.data = application.title #populate the form with the current application's title and content
        form.content.data = application.content 
    return render_template('create_application.html', title='Update Application', form=form, legend='Update Application')


@app.route("/application/<int:application_id>/delete", methods=['POST'])
@login_required
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    if application.author != current_user:
        abort(403)
    db.session.delete(application)
    db.session.commit()
    flash('Your application has been deleted!', 'success')
    return redirect(url_for('home'))

