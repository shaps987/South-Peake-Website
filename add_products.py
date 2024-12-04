from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from the .env file

app = Flask(__name__)

##CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///blog.db")

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

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

# CREATE RECORD
with app.app_context():
    new_product = Product(
        name = "Gyroscope",
        short_description = "This is a gyroscope. Gyroscopes are cool.",
        long_description = "This is a gyroscope. Gyroscopes are cool.",
        price = 3,
    )
    db.session.add(new_product)
    db.session.commit()
    new_image_link = ImageLink(
        img1 = "assets/img/product_images/gyroscope/gyro_img1.jpg",
        img2 = "assets/img/product_images/gyroscope/gyro_img2.jpg",
        img3 = "assets/img/product_images/gyroscope/gyro_img3.jpg",
        vid1 = "assets/img/product_images/gyroscope/gyro_vid1.mp4",
        product_id=new_product.id  # Associate the image link with the new product
        
    )
    db.session.add(new_image_link)
    db.session.commit()

    # Create a new product
    new_product = Product(
        name="Flexi-Rex",
        short_description = "Flexi-Rex is a multi-jointed t-rex. It is fun to fidget with and it can bend into many different stances.",
        long_description = "Flexi-Rex is a multi-jointed t-rex. It is fun to fidget with and it can bend into many different stances.",
        price=3,
    )
    db.session.add(new_product)
    db.session.commit()  # Commit to get the product ID

    # Create a new image link associated with the product
    new_image_link = ImageLink(
        img1="assets/img/product_images/flexi-rex/rex_img1.jpg",
        img2="assets/img/product_images/flexi-rex/rex_img2.jpg",
        img3="assets/img/product_images/flexi-rex/rex_img3.jpg",
        vid1="assets/img/product_images/flexi-rex/rex_vid1.mp4",
        product_id=new_product.id  # Associate the image link with the new product
    )
    db.session.add(new_image_link)
    db.session.commit()

    # Create a new product
    new_product = Product(
        name="Flexi-Octopus",
        short_description = "Flexi-Octopus is something something something something something.",
        long_description = "Flexi-Octopus is something something something something something.",
        price=3,
    )
    db.session.add(new_product)
    db.session.commit()  # Commit to get the product ID

    # Create a new image link associated with the product
    new_image_link = ImageLink(
        img1="assets/img/product_images/flexi-octopus/octopus_img1.jpg",
        img2="assets/img/product_images/flexi-octopus/octopus_img2.jpg",
        img3="assets/img/product_images/flexi-octopus/octopus_img3.jpg",
        vid1="assets/img/product_images/flexi-rex/rex_vid1.mp4",
        product_id=new_product.id  # Associate the image link with the new product
    )
    db.session.add(new_image_link)
    db.session.commit()

    # Create a new product
    new_product = Product(
        name="Flexi-Dragon",
        short_description = "Flexi-Dragon is something something something something something.",
        long_description = "Flexi-Dragon is something something something something something.",
        price=4,
    )
    db.session.add(new_product)
    db.session.commit()  # Commit to get the product ID

    # Create a new image link associated with the product
    new_image_link = ImageLink(
        img1="assets/img/product_images/flexi-dragon/dragon_img1.jpg",
        img2="assets/img/product_images/flexi-dragon/dragon_img2.jpg",
        img3="assets/img/product_images/flexi-dragon/dragon_img3.jpg",
        vid1="assets/img/product_images/flexi-rex/rex_vid1.mp4",
        product_id=new_product.id  # Associate the image link with the new product
    )
    db.session.add(new_image_link)
    db.session.commit()