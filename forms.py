from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email", check_deliverability=True)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm", message="The passwords provided do not match")])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email", check_deliverability=True)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email", check_deliverability=True)])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Contact South Peake")