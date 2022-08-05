from models import User, db, Post, PostTag, Tag
from app import app

db.drop_all()
db.create_all()

# add users
margaret = User(first_name = 'Margaret', last_name = 'Sun')
brenda = User(first_name = 'Brenda', last_name = 'Liu')

db.session.add(margaret)
db.session.add(brenda)

db.session.commit()

# add posts
margaret_post_1 = Post(title = 'My First Post', content = 'Look how cool this is', user_id = 1)
brenda_post_1 = Post(title = 'Selling Strawberries', content = '$99 each', user_id = 2)

db.session.add(margaret_post_1)
db.session.add(brenda_post_1)

db.session.commit()


# add tags

fun = Tag(name = 'fun')
happy = Tag(name = 'happy')

db.session.add(fun)
db.session.add(happy)

db.session.commit()