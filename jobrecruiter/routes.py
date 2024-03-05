
from flask import render_template, url_for, flash, redirect
from flask_login import current_user
from jobrecruiter import app, db, bcrypt
from jobrecruiter.forms import RegistrationForm, LoginForm
from jobrecruiter.models import User, Application
from flask_login import login_user

# The code below is dummy data, it gives me my application data
applications = [
    {
        'applicant': 'John Doe',
        'title': 'Application 1',
        'content': 'First job application ',
        'date_applied': 'April 20, 2018'
    },
    {
        'applicant': 'Lucas Afonso',
        'title': 'Application 2',
        'content': 'Second job application ',
        'date_applied': 'April 21, 2018'
    }
]



@app.route("/")
@app.route("/home") # This is a decorator

def home():
    return render_template('home.html', applications=applications)

@app.route("/about") 
def about():
    return render_template('about.html', title='About') # renders about.html template and passes title variable

@app.route("/register", methods=['GET', 'POST']) # This is a decorator
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): #if the submit is valid, flash the below message
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


