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

# CREATE RECORD
with app.app_context():
    new_product = Product(
        name = "Gyroscope",
        description = "This is a gyroscope. Gyroscopes are cool.",
        price = 3,
    )
    db.session.add(new_product)
    new_product = Product(
        img_one = "https://drive.google.com/file/d/1n_D5pYQS66us918CfPX3dEKa09sdzJmx/view?usp=drive_link",
        img_two = "https://drive.google.com/file/d/1chaQAcxWW1ZEDFGBuUKXUXPcjm3n2zRS/view?usp=sharing",
        img_three = "https://drive.google.com/file/d/1Rn7MZI9UOJjT29FXdsKxyS26o8eoO1_5/view?usp=drive_link",
        vid_one = "https://drive.google.com/file/d/1wN6KP6zyFP2eZSqCHpZDHkOECj6KOaig/view?usp=sharing",
        
    )
    db.session.add(new_product)
    db.session.commit()

    # Create a new product
    new_product = Product(
        name="Gyroscope2",
        description="This is a gyroscope2. Gyroscopes2 are cool.",
        price=3,
    )
    db.session.add(new_product)
    db.session.commit()  # Commit to get the product ID

    # Create a new image link associated with the product
    new_image_link = ImageLink(
        img_one="https://images.unsplash.com/photo-1729512680463-bc583c395b61?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D",
        img_two="https://images.unsplash.com/photo-1729582017869-a0c84b5c91b5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8Mnx8fGVufDB8fHx8fA%3D%3D",
        img_three="https://plus.unsplash.com/premium_photo-1728035716169-d0986b6bbfcf?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8M3x8fGVufDB8fHx8fA%3D%3D",
        vid_one="https://drive.google.com/file/d/1Q77DUfltmygKCOLJdAmM8DOGbi3lz3dw/view?usp=sharing",
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