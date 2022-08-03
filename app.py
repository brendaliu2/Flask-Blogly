"""Blogly application."""

from flask import Flask, redirect, render_template, render_template_string, request
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
    image_url = image_url if image_url else None

    new_user = User(first_name = first_name,
                    last_name = last_name,
                    image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<user_id>')
def display_user(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('user_id.html', user = user)


@app.get('/users/<user_id>/edit')
def display_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.post('/users/<user_id>/edit')
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    # TODO: refactor into a function in models?

    if request.form['first-name']:
        user.first_name = request.form['first-name']

    if request.form['last-name']:
        user.last_name = request.form['last-name']

    if request.form['image']:
     user.image_url = request.form['image']

    db.session.commit()

    return redirect('/users')


@app.post('/users/<user_id>/delete')
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    user.archived = True
    db.session.commit()

    return redirect('/users')








