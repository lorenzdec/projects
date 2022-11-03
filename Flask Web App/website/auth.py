from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# define this is a blueprint of our application
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filter all users that have the email we get from the form and then get the first user
        if user: #if we found a user, if it exists
            if check_password_hash(user.password, password): #check user.password from the db and password from the form against eachother
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #log in our user and remember this person is logged in, until they clear browser history/session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('User does not exist', category='error')

    #data = request.form  #request holds info about the request that was sent to access this root such as URL, method, form attributes, etc
    return render_template("login.html", user=current_user) #text is a variable name, we are passing through a string variable that then will show up on the page

@auth.route('/logout')
@login_required  #this makes it so the user cannot access this page unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if user does not already exist
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')

        elif len(first_name) < 2:
            flash('Email must be greater than 1 character.', category='error')

        elif password1 != password2:
            flash('Passwords don\'t match', category='error')

        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) #log in user after creating account
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) #redirect to home function in views blueprint


    return render_template("sign_up.html", user=current_user)