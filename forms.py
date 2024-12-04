from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
import os
import requests

class FlexibleIntegerField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0]) if valuelist[0].strip() != '' else 0
            except ValueError:
                raise ValidationError("This field requires an integer.")

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
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Contact South Peake")

class PurchaseForm(FlaskForm):
    gyroscopes = FlexibleIntegerField("# of Gyroscopes", validators=[InputRequired()])
    rexs = FlexibleIntegerField("# of Flexi-Rexs", validators=[InputRequired()])
    octopi = FlexibleIntegerField("# of Flexi-Octopi", validators=[InputRequired()])
    dragons = FlexibleIntegerField("# of Flexi-Dragons", validators=[InputRequired()])
    submit = SubmitField("Proceed to Order Summary")

class PurchaseConfirmationForm(FlaskForm):
    back = SubmitField("Edit")
    submit = SubmitField("Submit Order")