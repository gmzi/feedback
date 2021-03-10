from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """site user"""
    __tablename__ = "users"

    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    feedbacks = db.relationship('Feedback')

    @classmethod
    def register(cls, first_name, last_name, email, username, password):

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(first_name=first_name,
                   last_name=last_name, email=email, username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """validate user and password"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    """feedback posts"""
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # foreign key constraint
    username = db.Column(db.Text, db.ForeignKey(
        'users.username', ondelete='cascade'))
