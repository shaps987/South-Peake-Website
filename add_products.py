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
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    images = relationship("ImageLink", back_populates="product")

class ImageLink(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product = relationship("Product", back_populates="images")
    img1: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    img2: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    img3: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    vid1: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

with app.app_context():
    db.create_all()

# CREATE RECORD
with app.app_context():
    new_product = Product(
        name = "Gyroscope",
        description = "This is a gyroscope. Gyroscopes are cool.",
        price = 3,
    )
    db.session.add(new_product)
    new_product = Product(
        img1 = "https://drive.google.com/file/d/1n_D5pYQS66us918CfPX3dEKa09sdzJmx/view?usp=drive_link",
        img2 = "https://drive.google.com/file/d/1chaQAcxWW1ZEDFGBuUKXUXPcjm3n2zRS/view?usp=sharing",
        img3 = "https://drive.google.com/file/d/1Rn7MZI9UOJjT29FXdsKxyS26o8eoO1_5/view?usp=drive_link",
        vid1 = "https://drive.google.com/file/d/1wN6KP6zyFP2eZSqCHpZDHkOECj6KOaig/view?usp=sharing",
        
    )
    db.session.add(new_product)
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