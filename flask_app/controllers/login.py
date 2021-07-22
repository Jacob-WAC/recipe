from flask_app.models.users import User
from flask import render_template, redirect, request, session, flash
import re
from flask_app.controllers import main
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/registration', methods=['POST'])
def registration():

    if not User.validate_registration(request.form):
        return redirect('/')

    subscription = 0
    if 'subscription' in request.form:
        subscription = 1

    password_hashed = bcrypt.generate_password_hash(request.form['password'])
    print(password_hashed)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': password_hashed,
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'zip': request.form['zip'],
        'subscription': subscription
    }

    user_id = User.save(data)

    session['user_id'] = user_id
    session['user_name'] = data['first_name']
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    actual_user = User.get_user_by_email(data)
    if len(actual_user) == 0:
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    if not actual_user[0]:
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(actual_user[0].password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    session['user_id'] = actual_user[0].id
    session['user_name'] = actual_user[0].first_name
    return redirect('/dashboard')
