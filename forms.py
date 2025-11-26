from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class NoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Save")

class TaskForm(FlaskForm):
    title = StringField("Task", validators=[DataRequired()])
    submit = SubmitField("Add")
