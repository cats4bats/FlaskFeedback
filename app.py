from flask import Flask, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, LoginForm, FeedbackForm
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SECRET_KEY'] = 'the random string'    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


from models import User, Feedback
db.create_all()

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, password=pw_hash, email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()
        session['username'] = username
        return redirect('/secret')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        u = User.query.filter_by(username=username).first()

        if bcrypt.check_password_hash(u.password, password):
            session['username'] = username

        
        return redirect('/secret')
    return render_template('register.html', form=form)


@app.route('/secret')
def secret():
    if 'username' in session:
        return 'you made it'
    return 'you cant be here'

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/secret')

@app.route('/users/<username>')
def usernames(username):
    if 'username' in session:
        u = User.query.filter_by(username=username).first()
        feedbacks = Feedback.query.filter_by(username=username).all()
        return render_template('user.html', u=u, feedbacks=feedbacks)
    return 'you cant be here'

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if session['username'] == username:
        User.query.filter_by(username=username).delete()
        Feedback.query.filter_by(username=username).delete()
        db.session.commit()
        session.pop('username')
    return 'deleted'

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit() and session['username'] == username:
        title = form.title.data
        content = form.content.data
        
        f = Feedback(title=title, content=content, username=username)
        db.session.add(f)
        db.session.commit()
        
        return redirect(f'/users/{username}')
    if session['username'] == username:
        return render_template('add_feedback.html', form=form)
    return 'you cant do that'

@app.route('/feedback/<id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    f = Feedback.query.filter_by(id=id).first()
    username = f.username

    if session['username'] != username:
        return 'you cant be here'

    form = FeedbackForm(obj=f)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        f.title = title
        f.content = content
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<id>/delete', methods=['POST'])
def delete_feedback(id):
    f = Feedback.query.filter_by(id=id).first()
    username = f.username
    if session['username'] != username:
        return 'you cant be here'

    Feedback.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(f'/users/{username}')




