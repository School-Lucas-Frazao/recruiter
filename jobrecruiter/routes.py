from flask import render_template, url_for, flash, redirect
from jobrecruiter import app
from jobrecruiter.forms import RegistrationForm, LoginForm
from jobrecruiter.models import User, Application

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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) #redirects to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST']) # This is a decorator
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success') #success is a bootstrap class
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


