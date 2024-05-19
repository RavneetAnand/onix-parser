from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, exists
from onix_parser.models import Book, Country
from .database import session

# Function to add book only if isbn doesn't exist
def add_book(title, isbn):
    # Check if a book with the given isbn already exists
    book = session.query(Book).filter_by(isbn=isbn).first()

    if not book:
      # If not, create a new book instance and add it to the session
      book = Book(title=title, isbn=isbn)
      session.add(book)
      print("Book added successfully.")
    else:
      print("Book with this ISBN already exists.")

    session.commit()
    return book

def add_country(book, country_code):
    # Check if a country with the given code already exists
    country_exists = session.query(exists().where(and_(Country.country_code == country_code, Country.book_id  == book.id))).scalar()

    if not country_exists:
        # If not, create a new country instance and add it to the session
        country = Country(book_id=book.id, country_code=country_code)
        session.add(country)
        print("Country added successfully.")
    else:
        print("Country with this code already exists.")

    session.commit()
