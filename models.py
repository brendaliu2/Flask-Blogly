"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


DEFAULT_PIC = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1223671392?k=20&m=1223671392&s=612x612&w=0&h=lGpj2vWAI3WUT1JeJWm1PRoHT3V15_1pdcTn2szdwQ0='

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url= db.Column(db.String(),
                         nullable=True,
                         default = DEFAULT_PIC)
    archived = db.Column(db.Boolean,
                        nullable=False,
                        default = False)


    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    posts = db.relationship('Post')


class Post(db.Model):
    """Post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.String(),
                      nullable = False)
    content = db.Column(db.String(),
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default = db.func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    user = db.relationship('User')

    # post_tag = db.relationship('PostTag', backref= 'post')


# could have user id that is null line 56 (unknown author)


class Tag(db.Model):
    """PostTag"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name = db.Column(db.String(),
                      nullable = False,
                      unique = True)


    posts = db.relationship('Post',
                            secondary='post_tags',
                            backref='tags')

    # post_tag = db.relationship('PostTag', backref= 'tag')

class PostTag(db.Model):
    """Tag"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key = True)




