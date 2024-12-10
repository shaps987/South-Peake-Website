#--------------------------------------------------------------Imports--------------------------------------------------------------
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, ContactForm, PurchaseForm, PurchaseConfirmationForm
import os
from dotenv import load_dotenv
import smtplib
import requests

#--------------------------------------------------------------Load Env Variables from .env File--------------------------------------------------------------

with open("/etc/secrets/FLASK_KEY") as file:
    FLASK_KEY = file.read()
with open("/etc/secrets/RECAPTCHA_SITE_KEY") as file:
    RECAPTCHA_SITE_KEY = file.read()
with open("/etc/secrets/RECAPTCHA_SECRET_KEY") as file:
    RECAPTCHA_SECRET_KEY = file.read()
with open("/etc/secrets/TO_EMAIL") as file:
    TO_EMAIL = file.read()
with open("/etc/secrets/MY_EMAIL") as file:
    MY_EMAIL = file.read()
with open("/etc/secrets/APP_PASSWORD") as file:
    APP_PASSWORD = file.read()
with open("/etc/secrets/DB_URI") as file:
    DB_URI = file.read()

# load_dotenv()  # This loads the variables from the .env file
# FLASK_KEY = os.environ.get("FLASK_KEY")
# RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
# RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
# MY_EMAIL = os.environ.get("MY_EMAIL")
# APP_PASSWORD = os.environ.get("APP_PASSWORD")
# TO_EMAIL = os.environ.get("TO_EMAIL")
# DB_URI = os.environ.get("DB_URI", "sqlite:///blog.db")

#--------------------------------------------------------------Initiate Flask App/Initiate Bootstrap--------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_KEY
Bootstrap5(app)

#--------------------------------------------------------------Configure Flask-Login--------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)

#--------------------------------------------------------------Create Database--------------------------------------------------------------
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#--------------------------------------------------------------Configure Login and User System--------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

#--------------------------------------------------------------Configure Tables--------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    short_description = mapped_column(Text, unique=True, nullable=False)
    long_description: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    images = relationship("ImageLink", back_populates="product")

class ImageLink(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    img1: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    img2: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    img3: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    vid1: Mapped[str] = mapped_column(Text, unique=False, nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("products.id"))
    product = relationship("Product", back_populates="images")

with app.app_context():
    db.create_all()

#-----------------------------------------------------Configure Email Sending-----------------------------------------------------
def send_email(subject, message):
    email_message = f"Subject:{subject}\n\n{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, APP_PASSWORD)
        connection.sendmail(MY_EMAIL, TO_EMAIL, email_message)

#-----------------------------------------------------Condensed reCAPTCHA Verification----------------------------------------------
def verify_recaptcha(token):
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": RECAPTCHA_SECRET_KEY, "response": token}
    )
    return response.json().get("success", False)

#--------------------------------------------------------------Register Page--------------------------------------------------------------
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        recaptcha_token = request.form.get('recaptcha_token')
        if not verify_recaptcha(recaptcha_token):
            flash("Failed reCAPTCHA validation. Please try again.", "danger")
            return render_template("register.html", form=form, recaptcha_site_key=RECAPTCHA_SITE_KEY, logged_in=current_user.is_authenticated)

        user_exists = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user_exists:
            flash("You've already signed up with that email. Please log in instead.", "danger")
            return redirect(url_for('login'))

        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Registration successful!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form, recaptcha_site_key=RECAPTCHA_SITE_KEY, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Login Page--------------------------------------------------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        recaptcha_token = request.form.get('recaptcha_token')
        if not verify_recaptcha(recaptcha_token):
            flash("Failed reCAPTCHA validation. Please try again.", "danger")
            return render_template("login.html", form=form, recaptcha_site_key=RECAPTCHA_SITE_KEY, logged_in=current_user.is_authenticated)

        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for('login'))

        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for('index'))
    return render_template("login.html", form=form, recaptcha_site_key=RECAPTCHA_SITE_KEY, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Logout Process--------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#--------------------------------------------------------------Index Page (Home Page)--------------------------------------------------------------
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", current_user=current_user, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------About Page--------------------------------------------------------------
@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Contact Page--------------------------------------------------------------
@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Validate the reCAPTCHA token
        recaptcha_token = request.form.get('recaptcha_token')
        recaptcha_secret = os.getenv("RECAPTCHA_SECRET_KEY")
        recaptcha_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": recaptcha_secret, "response": recaptcha_token}
        )
        result = recaptcha_response.json()

        # Check if reCAPTCHA validation passed
        if not result.get("success"):
            flash("Failed reCAPTCHA validation. Please try again.", "danger")
            return render_template("contact.html", form=form, recaptcha_site_key=os.getenv("RECAPTCHA_SITE_KEY"), logged_in=current_user.is_authenticated)

        # Process the contact form
        message = f"""
        Name: {form.name.data}
        Email: {form.email.data}
        Phone Number: {form.phone.data}
        Message: {form.message.data}
        """
        send_email(subject="South Peake User Contacting You", message=message)
        flash("Your message has been sent successfully.", "success")
        return redirect(url_for("index"))
    
    return render_template("contact.html", form=form, recaptcha_site_key=os.getenv("RECAPTCHA_SITE_KEY"), logged_in=current_user.is_authenticated)


#--------------------------------------------------------------3D Printing Page--------------------------------------------------------------
@app.route('/3d_printing', methods=["GET", "POST"])
def printing():
    return render_template("3d_printing.html", logged_in=current_user.is_authenticated)

#--------------------------------------------------------------3D Printed Items--------------------------------------------------------------
@app.route('/3d_printing/items', methods=["GET", "POST"])
def items():
    result = db.session.execute(db.select(Product))
    products = result.scalars().all()
    return render_template("items.html", products=products, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Specific Item Page--------------------------------------------------------------
@app.route('/3d_printing/items/item', methods=["GET", "POST"])
def specific_item():
    id = request.args.get("id")
    item = db.get_or_404(Product, id)
    images = item.images[0]
    return render_template("specific_item.html", item=item, images=images, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Purchase Products Page--------------------------------------------------------------
@app.route('/3d_printing/purchase', methods=["GET", "POST"])
@login_required
def purchase():
    form = PurchaseForm()
    if form.validate_on_submit():
        global summary
        gyroscope_price = db.session.execute(db.select(Product).where(Product.name == "Gyroscope")).scalar().price
        rex_price = db.session.execute(db.select(Product).where(Product.name == "Flexi-Rex")).scalar().price
        octopus_price = db.session.execute(db.select(Product).where(Product.name == "Flexi-Octopus")).scalar().price
        dragon_price = db.session.execute(db.select(Product).where(Product.name == "Flexi-Dragon")).scalar().price
        session['summary'] = f"""
        # of Gyroscopes: {form.gyroscopes.data} \n
        # of Flexi-Rexs: {form.rexs.data} \n
        # of Flexi-Octopi: {form.octopi.data} \n
        # of Flexi-Dragons: {form.dragons.data} \n
        Cost: ${form.gyroscopes.data*gyroscope_price + form.rexs.data*rex_price + form.octopi.data*octopus_price + form.dragons.data*dragon_price}
        """
        return redirect(url_for("purchase_confirmation"))
    return render_template("purchase.html", form=form, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Purchase Confirmation Page--------------------------------------------------------------
@app.route('/3d_printing/purchase/confirmation', methods=["GET", "POST"])
@login_required
def purchase_confirmation():
    form = PurchaseConfirmationForm()
    summary=session.get('summary')
    if form.validate_on_submit():
        if form.back.data:  # Check if the "Edit" button was pressed
            return redirect(url_for('purchase'))  # Redirect to the purchase page
        elif form.submit.data:  # Check if the "Submit Order" button was pressed
            message="""
            Your order has been sent. Thank you for shopping with South Peake. We will process your order and reach out to the email associated with your account in order to make the transaction. Once again, we appreciate you for choosing South Peake.
            """
            email_messsage=f"""
            Summary: 
            {session.get('summary')}

            Account Email: { current_user.email }
            """
            
            send_email(subject="South Peake Order", message=email_messsage)
            return render_template("purchase_confirmation.html", message=message, form=form, summary=summary, logged_in=current_user.is_authenticated)

    return render_template("purchase_confirmation.html", form=form, summary=summary, logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Custom CAD Page--------------------------------------------------------------
@app.route('/3d_printing/cad', methods=["GET", "POST"])
def custom_cad():
    return render_template("custom_cad.html", logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Custom 3D Printing Page--------------------------------------------------------------
@app.route('/3d_printing/custom_3d', methods=["GET", "POST"])
def custom_printing():
    return render_template("custom_3d.html", logged_in=current_user.is_authenticated)

#--------------------------------------------------------------Web Design Page--------------------------------------------------------------
@app.route('/web_design', methods=["GET", "POST"])
def web_design():
    return render_template("web_design.html", logged_in=current_user.is_authenticated)

if __name__ == "__main__":
    app.run(debug=True)