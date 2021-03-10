from flask import Flask, session, flash
from sqlalchemy.exc import IntegrityError
from models import connect_db, db, User, Feedback


def permitted(username):
    """checks user permission to view and 
    manage feedbacks"""

    if 'username' not in session:
        flash('please login or register', 'error')
        return False
    if username == session['username']:
        return True
    return False


def fetch_from_db(Model, obj):
    result = Model.query.get_or_404(obj)
    return result
