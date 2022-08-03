"""Blogly application."""

from flask import Flask, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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


