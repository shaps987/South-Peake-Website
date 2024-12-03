from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class FlexibleIntegerField(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0]) if valuelist[0].strip() != '' else None
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
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email", check_deliverability=True)])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Contact South Peake")

class PurchaseForm(FlaskForm):
    gyroscopes = FlexibleIntegerField("# of Gyroscopes", validators=[DataRequired()])
    rexs = IntegerField("# of Flexi-Rexs", validators=[DataRequired()])
    octopi = IntegerField("# of Flexi-Octopi", validators=[DataRequired()])
    dragons = IntegerField("# of Flexi-Dragons", validators=[DataRequired()])
    submit = SubmitField("Proceed to Order Summary")

class PurchaseConfirmationForm(FlaskForm):
    back = SubmitField("Edit")
    submit = SubmitField("Submit Order")