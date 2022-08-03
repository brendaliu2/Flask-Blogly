from models import User, db
from app import app

db.drop_all()
db.create_all()

# add users
margaret = User(first_name = 'Margaret', last_name = 'Sun')
brenda = User(first_name = 'Brenda', last_name = 'Liu')

db.session.add(margaret)
db.session.add(brenda)

db.session.commit()