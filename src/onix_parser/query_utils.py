from sqlalchemy import and_, select
from src.database.models import Book, Country, book_country_association
from src.database.database import session
import logging

logging.basicConfig(level=logging.ERROR)


# Function to add book only if isbn doesn't exist
def add_book(title, isbn):
    try:
      # Check if a book with the given isbn already exists
      book = session.query(Book).filter_by(isbn=isbn).first()

      if not book:
        # If not, create a new book instance and add it to the session
        book = Book(title=title, isbn=isbn)
        session.add(book)
        session.commit()

      return book

    except Exception as e:
        session.rollback()
        logging.error(f"Failed to add books: {e}")

    finally:
        session.close()

def add_countries(book, country_codes):
    try:
      # Fetch all countries with the given country codes
      countries = session.query(Country).filter(Country.country_code.in_(country_codes)).all()

      # Check existing associations
      existing_associations = session.execute(
          select(book_country_association.c.country_id)
          .where(and_(
              book_country_association.c.book_id == book.id,
              book_country_association.c.country_id.in_([country.id for country in countries])
          ))
      ).fetchall()

      existing_country_ids = {row.country_id for row in existing_associations}

      # Prepare bulk insert for new associations
      new_associations = [
          {'book_id': book.id, 'country_id': country.id}
          for country in countries
          if country.id not in existing_country_ids
      ]

      if new_associations:
          session.execute(book_country_association.insert(), new_associations)

      session.commit()

    except Exception as e:
        session.rollback()
        logging.error(f"Failed to add countries: {e}")

    finally:
        session.close()

def get_countries_by_book(isbn):
    try:
      # Get the book id using isbn
      stmt = (
          select(Country.name)
          .select_from(Book)
          .join(book_country_association, Book.id == book_country_association.c.book_id)
          .join(Country, book_country_association.c.country_id == Country.id)
          .where(Book.isbn == isbn)
      )

      countries = session.execute(stmt).scalars().all()

      return countries

    except Exception as e:
        session.rollback()
        logging.error(f"Failed to get countries for the book: {e}")

    finally:
        session.close()
