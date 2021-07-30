from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class UserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('first name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('last name', validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class FeedbackForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=4, max=100)])
    content = StringField('content', validators=[InputRequired()])


