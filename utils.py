from flask import session
from sqlalchemy.exc import IntegrityError
from models import connect_db, db, User, Feedback


def authenticated(username):
    if 'username' not in session:
        return False
    if username == session['username']:
        return True
    return False
