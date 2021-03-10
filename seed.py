from models import db, User, Feedback
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# whiskey = Pet(name='Whiskey', species="dog")
jonas = User.register(first_name='jonas', last_name='Kaufman',
                      email='jonas@jonas.com', username='kaka', password='kaka')
paco = User.register(first_name='paco', last_name='rabanne', email='loco@loco.com',
                     username='oco', password='kaka')

f1 = Feedback(title='F1 title', content='f1 content is this', username='kaka')
f2 = Feedback(title='F2 title', content='f2 content is this', username='oco')


# Add new objects to session, so they'll persist
db.session.add(jonas)
db.session.add(paco)
db.session.add(f1)
db.session.add(f2)

# Commit to database
db.session.commit()

# run file: 'python seed.py', beware database will be erased
