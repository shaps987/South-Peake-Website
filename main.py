from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()  # This loads the variables from the .env file

app = Flask(__name__)
with open("/etc/secrets/FLASK_KEY") as file:
    FLASK_KEY = file.read()
app.config['SECRET_KEY'] = FLASK_KEY
Bootstrap5(app)

#Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

#Create Database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///blog.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#Configure Login and User System
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

#Configure Tables
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    short_description = mapped_column(Text, unique=False, nullable=False)
    long_description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    price: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    images = relationship("ImageLink", back_populates="product")

class ImageLink(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    img_one: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    img_two: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    img_three: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    vid_one: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("products.id"))
    product = relationship("Product", back_populates="images")

with app.app_context():
    db.create_all()

# Configure Email Sending
# with open("/etc/secrets/MY_EMAIL") as file:
#     MY_EMAIL = file.read()
# with open("/etc/secrets/TO_EMAIL") as file:
#     TO_EMAIL = file.read()
# with open("/etc/secrets/APP_PASSWORD") as file:
#     APP_PASSWORD = file.read()

# def send_email(subject, message):
#     email_message = f"Subject:{subject}\n\n{message}"
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(MY_EMAIL, APP_PASSWORD)
#         connection.sendmail(MY_EMAIL, TO_EMAIL, email_message)

#Register Page
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead.")
            return redirect(url_for('login'))
        
        
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8),
        )

        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        return redirect(url_for("index"))
    
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)

#Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('index'))
        
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)

#Logout Process
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Index Page (Home Page)
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", current_user=current_user, logged_in=current_user.is_authenticated)

#About Page
@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)

#Contact Page
@app.route('/contact', methods=["GET", "POST"])
def contact():
    return render_template("contact.html", logged_in=current_user.is_authenticated)

#3D Printing Page
@app.route('/3d_printing', methods=["GET", "POST"])
def printing():
    return render_template("3d_printing.html", logged_in=current_user.is_authenticated)

#3D Printed Toys
@app.route('/3d_printing/toys', methods=["GET", "POST"])
def toys():
    result = db.session.execute(db.select(Product))
    products = result.scalars().all()
    return render_template("toys.html", products=products, logged_in=current_user.is_authenticated)

#Specific Toy Page
@app.route('/3d_printing/toys/toy', methods=["GET", "POST"])
def specific_toy():
    id = request.args.get("id")
    return render_template("specific_toy.html", logged_in=current_user.is_authenticated)

#Custom CAD Page
@app.route('/3d_printing/cad', methods=["GET", "POST"])
def custom_cad():
    return render_template("custom_cad.html", logged_in=current_user.is_authenticated)

#Custom 3D Printing Page
@app.route('/3d_printing/custom_3d', methods=["GET", "POST"])
def custom_printing():
    return render_template("custom_3d.html", logged_in=current_user.is_authenticated)

#Web Design Page
@app.route('/web_design', methods=["GET", "POST"])
def web_design():
    return render_template("web_design.html", logged_in=current_user.is_authenticated)

if __name__ == "__main__":
    app.run(debug=True)