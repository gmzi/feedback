from flask_wtf import FlaskForm
from werkzeug.wrappers import UserAgentMixin
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Optional


class UserForm(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    email = StringField("Email", validators=[Optional(), Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Text", validators=[InputRequired()])
