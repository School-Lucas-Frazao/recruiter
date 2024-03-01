from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

# This is a secret key that is used to protect the application from attacks like CSRF
app.config['SECRET_KEY'] = 'c7b9d1d86846390b91fa1ef4d27172d0'

# The code below is dummy data, it gives me my application data
application = [
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
    return render_template('home.html', application=application)

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
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__': # This is a conditional statement so you can run the app
    app.run(debug=True)

    