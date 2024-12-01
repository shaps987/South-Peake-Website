from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

    img1: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    img2: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    img3: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    vid1: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

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

# #READ All Records
# with app.app_context():
#     all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()

# #READ a Particular Record By Query
# with app.app_context():
#     book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter Book 1")).scalar() #Using .scalar(), not .scalars()

# #UPDATE A Particular Record By Query
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter Book 2")).scalar()
#     book_to_update.title = "Harry Potter and the Chamber of Secrets"
#     db.session.commit() 

# #UPDATE A Record By Primary Key
# book_id = 2
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     # or book_to_update = db.get_or_404(Book, book_id)  
#     book_to_update.title = "Harry Potter and the Sorcerer's Stone"
#     db.session.commit()
    
# #DELETE A Particular Record by Primary Key
# book_id = 1
# with app.app_context():
#     book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     # or book_to_delete = db.get_or_404(Book, book_id)
#     db.session.delete(book_to_delete)
#     db.session.commit()