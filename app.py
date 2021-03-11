from flask import Flask, render_template, redirect, session, flash
from models import Feedback, connect_db, db, User
from sqlalchemy.exc import IntegrityError
from forms import UserForm, LoginForm, FeedbackForm
from utils import permitted, fetch_from_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "123123"


connect_db(app)

# Reload with no cache for styling purposes:


@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')
    else:
        username = session['username']
        return redirect(f"/users/{username}")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """register user, grab user data and process in db"""
    form = UserForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User.register(first_name=first_name, last_name=last_name,
                                 email=email, username=username, password=password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken')
            return render_template('register.html', form=form)

        session['username'] = new_user.username
        flash('Welcome', 'success')
        return redirect(f"/users/{username}")
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{username}")
        else:
            form.password.errors = ['Bad name or pass']
    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    """shows route only to logged in users"""
    if 'username' not in session:
        flash('must login or register to view')
        return redirect('/')
    if permitted(username):
        user = User.query.get_or_404(username)
        feedbacks = user.feedbacks
        return render_template('secret.html', user=user, feedbacks=feedbacks)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username')
    flash('goodbye', 'info')
    return redirect('/')


@app.route('/users/<username>/delete')
def user_delete(username):
    # TODOS: display warning before deleting user.
    if permitted(username):
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        flash(f"Bye bye {user.username}, see you around", 'info')
        session.pop('username')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedb_add(username):
    if permitted(username):
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_fb = Feedback(title=title, content=content,
                              username=username)
            db.session.add(new_fb)
            try:
                db.session.commit()
            except Exception as Error:
                db.session.rollback()
                return 'oh no'
            flash('feedback added!!!', 'success')
            return redirect('/')
        else:
            return render_template('fb-form.html', form=form)
    else:
        flash('please login or register', 'error')
        return redirect('/')


@app.route('/feedback/<int:fb_id>/update', methods=["GET", "POST"])
def feedback_update(fb_id):
    fb = fetch_from_db(Feedback, fb_id)
    username = fb.username
    if permitted(username):

        form = FeedbackForm(obj=fb)

        if form.validate_on_submit():
            fb.title = form.title.data
            fb.content = form.content.data
            db.session.commit()
            flash("it's updated", 'success')
            return redirect(f"/users/{username}")
        else:
            return render_template('fb-form.html', form=form)
    else:
        flash('not in your feedback list', 'error')
        return redirect('/')


@app.route('/feedback/<int:fb_id>/delete')
def feedback_delete(fb_id):
    fb = fetch_from_db(Feedback, fb_id)
    username = fb.username
    if permitted(username):
        # TODOS: display warning before deleting
        db.session.delete(fb)
        db.session.commit()
        flash("it's gone", 'sucess')
        return redirect(f"/users/{username}")
    else:
        flash('must own fb to delete it', 'error')
        return redirect('/')
