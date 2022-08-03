"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = 'secret_key'
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def redirect_to_users():
    return redirect('/users')

@app.get('/users')
def show_all_users():
    users = User.query.all()
    return render_template('user.html', users = users)

@app.get('/users/new')
def display_new_user_form():
    return render_template('new_user.html')

@app.post('/users/new')
def add_new_user():

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image']

    new_user = User(first_name = first_name,
                    last_name = last_name,
                    image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<user_id>')
def display_user(user_id):

    user = User.query.get(user_id)

    return render_template('user_id.html', user = user)