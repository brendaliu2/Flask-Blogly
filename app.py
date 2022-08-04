"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post
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
    """Redirect to a list of users"""
    return redirect('/users')

@app.get('/users')
def show_all_users():
    """Displays list of users page"""
    users = User.query.all()

    return render_template('user.html', users = users)

@app.get('/users/new')
def display_new_user_form():
    """Displays new user form"""
    return render_template('new_user.html')

@app.post('/users/new')
def add_new_user():
    """Adds new users and redirect to list of users page"""

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
    """Displays current user"""

    user = User.query.get_or_404(user_id)

    posts = Post.query.filter(Post.user_id == user_id)

    return render_template('user_id.html', user = user, posts = posts)

@app.get('/users/<user_id>/edit')
def display_edit_form(user_id):
    """Displays edit form for current user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.post('/users/<user_id>/edit')
def edit_user(user_id):
    """Makes changes to current user's data"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image']

    db.session.commit()

    return redirect('/users')


@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    """Archives user and redirects to list of users page"""

    user = User.query.get_or_404(user_id)
    # user.archived = True
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<user_id>/posts/new')
def show_new_post_form(user_id):
    """Displays new post form"""

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user = user)

@app.post('/users/<user_id>/posts/new')
def add_new_post(user_id):
    """Adds new post for user"""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title = title,
                    content = content,
                    user_id = user_id)

    db.session.add(new_post)
    db.session.commit()


    return redirect (f'/users/{user_id}')

@app.get('/posts/<post_id>')
def show_post(post_id):
    """Shows user's post"""

    post = Post.query.get_or_404(post_id)

    return render_template('/show_post.html', post = post)

@app.get('/posts/<post_id>/edit')
def show_edit_post_form(post_id):
    """Displays edit post page"""

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post = post)


@app.post('/posts/<post_id>/edit')
def edit_post(post_id):
    """Makes edits to existing post"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.post('/posts/<post_id>/delete')
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

